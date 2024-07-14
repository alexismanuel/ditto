# ditto: dependency injection tool

ditto is a simple and lightweight dependency injection tool for Python, with support for nullable arguments and parent class registration.

## Features

- Easy-to-use decorators for dependency injection
- Supports class and instance-based services
- Sync and Async support
- Nullable argument handling
- Parent class registration

## Installation

```sh
pip install pyditto
```

## Usage

### Basic Usage

Declare your dependencies to ditto on application start:

```python
import ditto as di

class Pokemon:
    def attack(self) -> str:
        pass

class FirePokemon(Pokemon):
    def attack(self) -> str:
        return 'Ember ! 🔥'

di.register(FirePokemon)  # register as a class
di.register(FirePokemon())  # or as an object
```

Then you can inject your dependency into your class:

```python
@di.inject
class Team:
    charmander: FirePokemon

    def battle(self):
        self.charmander.attack()

team = Team()
team.battle()  # 'Ember ! 🔥'
```

Or into an isolated function within your class:

```python
class Team:
    @di.inject
    def battle(self, charmander: FirePokemon):
        charmander.attack()

team = Team()
team.battle()  # 'Ember ! 🔥'
```

Or just within a bare function:

```python
@di.inject
def battle(charmander: FirePokemon):
    charmander.attack()

battle()  # 'Ember ! 🔥'
```

## Advanced Usage

### Type Lookup in Registry

ditto uses the lowercase name of the class as the key in its registry:

```python
di.register(Charmander)

# These will all retrieve the Charmander instance:
fire_pokemon = di.ServiceRegistry.get_instance().get('firepokemon')
charmander = di.ServiceRegistry.get_instance().get('charmander')
```

This is particularly useful to understand when working with optional dependencies or when overriding parent class implementations.

### Asynchronous Support

ditto supports dependency injection for asynchronous functions:

```python
import asyncio

class AsyncPokemon:
    async def attack(self) -> str:
        await asyncio.sleep(1)
        return "Async attack!"

di.register(AsyncPokemon)

@di.inject
async def async_battle(pokemon: AsyncPokemon):
    result = await pokemon.attack()
    print(result)

asyncio.run(async_battle())  # Output: Async attack!
```

### Nullable Argument Handling

ditto supports nullable arguments, allowing you to specify optional dependencies:

```python
from typing import Optional

@di.inject
def train_pokemon(charmander: FirePokemon, optional_pokemon: Optional[Pokemon] = None):
    charmander.attack()
    if optional_pokemon:
        optional_pokemon.attack()
    else:
        print("No optional Pokemon available")

# This will work even if Pokemon is not registered
train_pokemon()

# You can also explicitly pass None for optional arguments
train_pokemon(optional_pokemon=None)
```

In this example:
- `charmander` is a required dependency and must be registered.
- `optional_pokemon` is an optional dependency. If it's not registered, `None` will be injected.

**Note on Type Registration for Optional Parameters:**
For both `Pokemon` and `Optional[Pokemon]`, ditto uses the same key (`'pokemon'`) in its registry. The `Optional` wrapper doesn't affect the registration key; it only changes how ditto handles the case when the service isn't found.

### Parent Class Registration

When you register a service class, ditto automatically registers it under its immediate parent class as well:

```python
class Pokemon:
    pass

class FirePokemon(Pokemon):
    pass

class Charmander(FirePokemon):
    pass

di.register(Charmander)

@di.inject
def train(fire_pokemon: FirePokemon, charmander: Charmander):
    print(f"Training: {fire_pokemon.__class__.__name__}, {charmander.__class__.__name__}")

train()  # Output: Training: Charmander, Charmander

@di.inject
def catch(pokemon: Pokemon):
    print(f"Trying to catch: {pokemon.__class__.__name__}")

catch()  # This will raise a ValueError: Service 'pokemon' not found.
```

In this example:
- Registering `Charmander` also makes it available when `FirePokemon` (its immediate parent class) is requested.
- However, `Pokemon` (the grandparent class) is not automatically registered.
- This allows for one level of inheritance in dependency injection.


### Error Handling and Common Pitfalls

1. Missing dependencies:
   If a required dependency is not registered, ditto will raise a `ValueError`:

   ```python
   @di.inject
   def use_unregistered(service: NotInPokedexPokemon):
       pass

   use_unregistered()  # Raises ValueError: Service 'notinpokedexpokemon' not found.
   ```

2. Circular dependencies:
   ditto doesn't automatically resolve circular dependencies. Be cautious when designing your dependency graph.

### Multiple Registrations

When multiple classes are registered for the same type, ditto will use the most recently registered one:

```python
class Pikachu(Pokemon):
    pass

class Charmander(Pokemon):
    pass

di.register(Pikachu)
di.register(Charmander)

@di.inject
def catch(pokemon: Pokemon):
    print(f"Caught a {pokemon.__class__.__name__}")

catch()  # Output: Caught a Charmander
```

### Best Practices

1. Register dependencies at the application's entry point.
2. Use interfaces (abstract base classes) for better decoupling.
3. Avoid registering too many concrete implementations to keep your dependency graph simple.

### Managing Registered Services

To unregister a service:

```python
# Unregister a service
ServiceRegistry.get_instance()._services.pop('pokemon', None)

```

## Limitations

- ditto doesn't support automatic constructor injection. Parameters must be explicitly annotated.
- Circular dependencies are not automatically resolved and may cause issues if not carefully managed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
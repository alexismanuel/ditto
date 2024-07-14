# ditto: dependency injection tool

ditto is a simple and lightweight dependency injection tool for Python, now with support for nullable arguments.

## Features

- Easy-to-use decorators for dependency injection
- Supports class and instance-based services
- Sync and Async support
- Nullable argument handling

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

### Nullable Argument Handling

ditto now supports nullable arguments, allowing you to specify optional dependencies:

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
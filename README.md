# ditto: dependency injection tool

ditto is a simple and lightweight dependency injection tool for Python.

## Features

- Easy-to-use decorators for dependency injection.
- Supports class and instance-based services.
- Sync and Async support

## Installation

```sh
pip install pyditto
```

## Usage
Declare your dependencies to ditto on application start.

```python
import ditto as di

class Pokemon:
    def attack(self) -> str:
        pass

class FirePokemon(Pokemon):
    def attack(self) -> str:
        return 'Ember ! 🔥'

di.register(FirePokemon) # register as a class
di.register(FirePokemon()) # or as an object
```

Then you can inject your dependency into your class:
```python
@di.inject
class Team:
    charmander: FirePokemon

    def battle(self):
        self.charmander.attack()



team = Team()
team.battle() # 'Ember ! 🔥'
```
Or into an isolated function within your class:
```python
class Team:
    
    @di.inject
    def battle(self, charmander: FirePokemon):
        self.charmander.attack()

team = Team()
team.battle() # 'Ember ! 🔥'

```
Or just within a bare function:
```python
@di.inject
def battle(charmander: FirePokemon):
    self.charmander.attack()

battle() # 'Ember ! 🔥'
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

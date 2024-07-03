# ditto: dependency injection tool

ditto is a simple and lightweight dependency injection tool for Python.

## Installation

```sh
pip install ditto
```

## Usage
```python
from ditto.core import ServiceRegistry

registry = ServiceRegistry.get_instance()

class Service:
    pass

registry.register('service', Service)
service = registry.get('service')
```

from __future__ import annotations
import inspect
from functools import wraps


def inject(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if name not in kwargs and param.default == inspect.Parameter.empty:
                kwargs[name] = ServiceRegistry.get_instance().get(name)
        return func(*args, **kwargs)

    return wrapper


def register(service):
    registry = ServiceRegistry.get_instance()
    service_class = service if inspect.isclass(service) else service.__class__
    base_class = service_class.__bases__.get(0, service_class)
    registry.register(base_class, service)


class ServiceRegistry:
    __slots__ = ('_services',)
    instance = None

    def __init__(self):
        self._services = {}

    def register(self, service_name, provider):
        self._services[service_name] = provider

    def get(self, service_name):
        provider = self._services.get(service_name)
        if not provider:
            raise ValueError(f'Service {service_name} not found')
        return provider()

    @classmethod
    def get_instance(cls) -> ServiceRegistry:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance


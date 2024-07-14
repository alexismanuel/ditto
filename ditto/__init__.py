from __future__ import annotations
import inspect
from functools import wraps
from typing import Type, Any, Callable, Union, Optional, get_origin, get_args


class ServiceRegistry:
    """Singleton service registry for dependency injection."""

    __slots__ = ('_services',)
    instance: ServiceRegistry | None = None

    def __init__(self) -> None:
        self._services: dict[str, Union[Type, Callable[[], Any]]] = {}

    def register(self, service_class: Type, provider: Union[Type, Callable[[], Any]]) -> None:
        """
        Register a service with the registry.

        :param service_class: The base class or interface of the service.
        :param provider: The concrete implementation or an instance of the service.
        """
        key = service_class.__name__.lower()
        self._services[key] = provider

    def get(self, service_name: str) -> Any:
        """
        Retrieve a service from the registry.

        :param service_name: The name of the service class.
        :return: An instance of the requested service.
        :raises ValueError: If the service is not found.
        """
        key = service_name.lower()
        provider = self._services.get(key)
        if not provider:
            raise ValueError(f"Service '{service_name}' not found.")
        return provider() if callable(provider) else provider

    @classmethod
    def get_instance(cls) -> ServiceRegistry:
        """Retrieve the singleton instance of the registry."""
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance


def is_optional(annotation: Any) -> bool:
    """Check if a type annotation is Optional."""
    origin = get_origin(annotation)
    if origin is Union:
        args = get_args(annotation)
        return type(None) in args
    return False

def get_base_type(annotation: Any) -> Type:
    """Get the base type from an Optional annotation."""
    if is_optional(annotation):
        args = get_args(annotation)
        return next(arg for arg in args if arg is not type(None))
    return annotation

def inject(func: Callable) -> Callable:
    """
    Decorator to inject dependencies into a function,
    with support for nullable arguments.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs)
        for name, param in sig.parameters.items():
            if name in bound_args.arguments:
                continue
            if param.annotation == inspect.Parameter.empty:
                if param.default == inspect.Parameter.empty:
                    raise ValueError(f"Missing type annotation for parameter '{name}'")
                continue
            
            is_nullable = is_optional(param.annotation) or param.default is None
            base_type = get_base_type(param.annotation)
            service_name = base_type.__name__.lower()
            
            try:
                service = ServiceRegistry.get_instance().get(service_name)
                kwargs[name] = service
            except ValueError:
                if is_nullable:
                    kwargs[name] = None
                else:
                    raise ValueError(f"Required service '{service_name}' not found.")
        
        return func(*args, **kwargs)

    return wrapper

def register(service: Any) -> None:
    """
    Register a service with the registry.
    If a service inherits from a parent class, the parent class is also registered.

    :param service: The service class or instance to register.
    """
    registry = ServiceRegistry.get_instance()
    service_class = service if inspect.isclass(service) else service.__class__
    parent_class = service_class.__bases__[0]
    
    if parent_class.__name__ != 'object':
        registry.register(parent_class, service)
    
    registry.register(service_class, service)
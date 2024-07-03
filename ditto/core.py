from __future__ import annotations


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

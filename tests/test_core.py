from ditto.core import ServiceRegistry
import pytest


class TestServiceRegistry:
    def test_register_and_get_service(self):
        registry = ServiceRegistry.get_instance()

        class Service:
            pass

        registry.register('service', Service)
        service = registry.get('service')
        assert isinstance(service, Service)

    def test_get_nonexistent_service(self):
        registry = ServiceRegistry.get_instance()

        with pytest.raises(ValueError):
            registry.get('nonexistent_service')

    def test_singleton_instance(self):
        instance1 = ServiceRegistry.get_instance()
        instance2 = ServiceRegistry.get_instance()
        assert instance1 == instance2

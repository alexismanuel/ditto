import pytest
from typing import Optional
from ditto import ServiceRegistry, register, inject, is_optional, get_base_type

class Meta:
    def greet(self) -> str:
        pass

class Service(Meta):
    def __init__(self) -> None:
        self.msg = 'hello'

    def greet(self) -> str:
        return self.msg

class AnotherService:
    def __init__(self) -> None:
        self.msg = 'world'

    def greet(self) -> str:
        return self.msg

class AsyncService:
    def __init__(self) -> None:
        self.msg = 'async'

    async def greet(self) -> str:
        return self.msg

@pytest.fixture
def registry() -> ServiceRegistry:
    return ServiceRegistry()

class TestServiceRegistry:
    def test_register_and_get_service(self, registry: ServiceRegistry):
        registry.register(Service, Service)
        service = registry.get('service')
        assert isinstance(service, Service)

    def test_register_and_get_instance(self, registry: ServiceRegistry):
        service_instance = Service()
        registry.register(Service, service_instance)
        service = registry.get('service')
        assert service is service_instance

    def test_get_nonexistent_service(self, registry: ServiceRegistry):
        with pytest.raises(ValueError, match="Service 'nonexistent' not found."):
            registry.get('nonexistent')

class TestRegister:
    def test_register_service_class(self):
        register(Service)
        service = ServiceRegistry.get_instance().get('service')
        assert isinstance(service, Service)

    def test_register_service_instance(self):
        service_instance = Service()
        register(service_instance)
        service = ServiceRegistry.get_instance().get('service')
        assert service is service_instance

    def test_register_service_with_parent_class(self):
        register(Service)
        service = ServiceRegistry.get_instance().get('meta')
        assert isinstance(service, Service)

class TestInject:
    @inject
    def greet_service(self, service: Meta) -> str:
        return service.greet()

    @inject
    def greet_another_service(self, service: AnotherService) -> str:
        return service.greet()

    @inject
    def greet_without_annotation(self, service) -> str:
        return service.greet()
    
    @inject
    async def async_greet_service(self, service: AsyncService) -> str:
        return await service.greet()

    @inject
    def greet_nullable_service(self, service: Optional[AnotherService] = None) -> str:
        return service.greet() if service else "No service"
    
    @inject
    def function_with_unannotated_service(self, service):
        return service.greet()
    
    @inject
    def function_with_unannotated_service_and_default(self, service=None):
        return service

    def test_inject_with_registered_service(self):
        register(Service)
        res = self.greet_service()
        assert res == 'hello'

    def test_inject_with_multiple_registered_services(self):
        register(Service)
        register(AnotherService)
        res = self.greet_service()
        second_res = self.greet_another_service()
        assert res == 'hello'
        assert second_res == 'world'

    def test_inject_missing_type_annotation(self):
        register(Service)
        with pytest.raises(ValueError, match="Missing type annotation for parameter 'service'"):
            self.greet_without_annotation()

    def test_inject_service_not_found(self):
        ServiceRegistry.instance = None
        with pytest.raises(ValueError, match="Required service 'meta' not found."):
            self.greet_service()
    
    @pytest.mark.asyncio
    async def test_inject_async_service(self):
        register(AsyncService)
        res = await self.async_greet_service()
        assert res == 'async'

    def test_inject_nullable_service_when_registered(self):
        register(AnotherService)
        res = self.greet_nullable_service()
        assert res == 'world'

    def test_inject_nullable_service_when_not_registered(self):
        ServiceRegistry.instance = None
        res = self.greet_nullable_service()
        assert res == 'No service'

    def test_inject_nullable_service_with_explicit_none(self):
        register(AnotherService)
        res = self.greet_nullable_service(service=None)
        assert res == 'No service'
    
    def test_inject_with_unannotated_service(self):
        with pytest.raises(ValueError, match="Missing type annotation for parameter 'service'"):
            self.function_with_unannotated_service()
    
    def test_inject_with_unannotated_param_and_default(self):
        result = self.function_with_unannotated_service_and_default()
        assert result is None

class TestUtilityFunctions:
    def test_is_optional(self):
        assert is_optional(Optional[int])
        assert is_optional(Optional[Service])
        assert not is_optional(int)
        assert not is_optional(Service)

    def test_get_base_type(self):
        assert get_base_type(Optional[int]) == int
        assert get_base_type(Optional[Service]) == Service
        assert get_base_type(int) == int
        assert get_base_type(Service) == Service

@pytest.fixture(autouse=True)
def clear_registry():
    yield
    ServiceRegistry.instance = None
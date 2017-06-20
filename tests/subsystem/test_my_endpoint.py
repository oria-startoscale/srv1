import waiting

from tests.subsystem.base import SubsystemBaseTest
from srv1.consts import my_endpoint_status


class TestMyEndpoint(SubsystemBaseTest):
    """srv1 tests."""

    def test_my_endpoint_happy_flow(self):
        """Validate srv1 api - happy flow."""
        created_resource = self.srv1.my_endpoint.create(name='test-resource')
        waiting.wait(
            lambda: self.srv1.my_endpoint.get(created_resource.id)['status'] == my_endpoint_status.FINISHED,
            sleep_seconds=2,
            timeout_seconds=60
        )
        created_resource['status'] = my_endpoint_status.FINISHED
        created_resource['result'] = 'provisioning_result'
        get_resource = self.srv1.my_endpoint.get(created_resource.id)
        self.assertEquals(created_resource, get_resource)
        self.srv1.my_endpoint.delete(created_resource.id)
        self.assertNotIn(created_resource.id,
                         [resource.id for resource in self.srv1.my_endpoint.list()])

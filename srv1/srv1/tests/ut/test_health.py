# pylint: disable=attribute-defined-outside-init
import httplib
import hammock.common as common

from tests.ut.base import BaseTest


class HealthTest(BaseTest):
    """Test health resource APIs."""

    def test_get(self):
        """Validate health resource 'get' API."""
        expected_response = {'status': 'healthy'}

        health_response = self.assert_status(
            httplib.OK,
            common.GET,
            '/api/v2/srv1/health/'
        )
        self.assertEqual(health_response, expected_response)

# pylint: disable=attribute-defined-outside-init
import httplib
import mock
import munch
import uuid

import hammock.common as common

from tests.ut.base import BaseTest


@mock.patch("celery.app.task.Task.delay", mock.MagicMock(return_value=munch.Munch(id=str(uuid.uuid4()))))
class MyEndpointTest(BaseTest):
    """Test My Endpoint resource APIs."""

    def test_create(self):
        """Validate My Endpoint resource 'create' API."""
        self.assert_status(
            httplib.ACCEPTED,
            common.POST,
            '/api/v2/srv1/my-endpoint',
            body={'name': 'test-name'}
        )

    def test_get(self):
        """Validate My Endpoint resource 'get' API."""
        # Get my_endpoint resource and validate no my_endpoint resource was found
        self.assert_status(httplib.NOT_FOUND, common.GET, '/api/v2/srv1/my-endpoint/1')

        # Create a new my_endpoint resource
        create_response = self.assert_status(
            httplib.ACCEPTED,
            common.POST,
            '/api/v2/srv1/my-endpoint',
            body={'name': 'test-name'}
        )

        # Get the created resource and validate it was found
        get_response = self.assert_status(
            httplib.OK,
            common.GET,
            '/api/v2/srv1/%(res_name)s/%(res_id)s' %
            dict(res_name='my-endpoint', res_id=create_response['id']),
        )
        self.assertEqual(create_response, get_response)

    def test_list(self):
        """Validate My Endpoint resource 'list' API."""
        # List my_endpoint resource and validate no my_endpoint resource was found
        list_response = self.assert_status(
            httplib.OK,
            common.GET,
            '/api/v2/srv1/my-endpoint',
        )
        self.assertEqual(len(list_response), 0)

        # Create a new my_endpoint resource
        create_response = self.assert_status(
            httplib.ACCEPTED,
            common.POST,
            '/api/v2/srv1/my-endpoint',
            body={'name': 'test-name'}
        )

        # List my_endpoint resources and validate one my_endpoint resource was found
        list_response = self.assert_status(
            httplib.OK,
            common.GET,
            '/api/v2/srv1/my-endpoint',
        )
        self.assertEqual(len(list_response), 1)
        self.assertIn(create_response, list_response)

    def test_delete(self):
        """Validate My Endpoint resource 'delete' API."""
        # Delete a missing my_endpoint resource and validate it was not found
        self.assert_status(
            httplib.NOT_FOUND,
            common.DELETE,
            '/api/v2/srv1/my-endpoint/1',
        )

        # Create a new my_endpoint resource then delete it and validate success
        create_response = self.assert_status(
            httplib.ACCEPTED,
            common.POST,
            '/api/v2/srv1/my-endpoint',
            body={'name': 'test-name'}
        )

        # Delete the created resource and validate success
        self.assert_status(
            httplib.NO_CONTENT,
            common.DELETE,
            '/api/v2/srv1/%(res_name)s/%(res_id)s' %
            dict(res_name='my-endpoint', res_id=create_response['id']),
        )

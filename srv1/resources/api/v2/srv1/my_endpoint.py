import httplib

import hammock
from strato_common.service_utils.db.resource_base import ResourceBase

from srv1.managers import my_endpoint


class MyEndpoint(ResourceBase):
    """My Endpoint resource APIs."""

    @hammock.post(success_code=httplib.ACCEPTED)
    def create(self, _credentials, name):
        """Creates a new my_endpoint object.

        :param str name: Name of the new my_endpoint
        :return dict: My_endpoint response
        """
        record = my_endpoint.MyEndpointManager(
            db_engine=self.db_engine, credentials=_credentials).create(name)
        return record.to_dict()

    @hammock.get("{my_endpoint_id}")
    def get(self, _credentials, my_endpoint_id):
        """Returns a my_endpoint based on a my_endpoint ID.

        :param str my_endpoint_id: ID of the requested my_endpoint object
        :return dict: My_endpoint response
        """
        return my_endpoint.MyEndpointManager(
            db_engine=self.db_engine, credentials=_credentials).get(my_endpoint_id).to_dict()

    @hammock.get()
    def list(self, _credentials):
        """Returns all my_endpoint objects.

        :return list: My_endpoint objects
        """
        return [record.to_dict() for record in
                my_endpoint.MyEndpointManager(
                db_engine=self.db_engine, credentials=_credentials).list()]

    @hammock.delete("{my_endpoint_id}", success_code=httplib.NO_CONTENT)
    def delete(self, _credentials, my_endpoint_id):
        """Deletes a single my_endpoint object based on the ID supplied.

        :param str my_endpoint_id: ID of the requested my_endpoint object
        """
        my_endpoint.MyEndpointManager(
            db_engine=self.db_engine, credentials=_credentials).delete(my_endpoint_id)

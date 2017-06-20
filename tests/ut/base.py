import hammock.testing as hammock_testing
from strato_common.credentials import StratoCredentials
import strato_consts.apiconfig as api_config

from srv1.db.models.my_endpoint import MyEndpointModel
from strato_common.service_utils.db.sqlite_memory_engine import create_db_engine


class BaseTest(hammock_testing.TestBase):

    RESOURCES = 'srv1.resources'
    CREDENTIAL_CLASS = StratoCredentials

    # Headers attributes and data
    TEST_ADMIN_ROLES = 'admin;tenant_admin;member'
    TEST_MEMBER_ROLES = '_member_'
    TEST_PROJECT_ID = '87b5adefe8e04f8dbb5a61fd9669fefd'
    TEST_USER_ID = '87b5adefe8e04f8dbb5a61fd9669fhgf'

    HEADERS_ADMIN = {
        api_config.StratoHttpHeaders.USER_ROLES: TEST_ADMIN_ROLES,
        api_config.StratoHttpHeaders.PROJECT_ID: TEST_PROJECT_ID,
        api_config.StratoHttpHeaders.USER_ID: TEST_USER_ID,
    }

    def setUp(self):
        # other models, if exist, need to be added here
        db_engine = create_db_engine([MyEndpointModel])
        self.RESOURCE_PARAMS = {'db_engine': db_engine}
        super(BaseTest, self).setUp()

    def assert_status(self, status, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.HEADERS_ADMIN
        return super(BaseTest, self).assert_status(status, *args, **kwargs)

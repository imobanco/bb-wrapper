from unittest.mock import patch, MagicMock, Mock

from tests.utils import IsolatedEnvTestCase, MockedBBTestCase
from bb_wrapper.wrapper.bb import BaseBBWrapper


class BaseBBWrapperTestCase(IsolatedEnvTestCase, MockedBBTestCase):
    def test_authenticate(self):
        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            401, data={"access_token": "access_token", "token_type": "token_type"}
        )

        result = BaseBBWrapper()._BaseBBWrapper__authenticate()

        self.assertEqual(result, True)

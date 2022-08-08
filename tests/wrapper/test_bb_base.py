from unittest.mock import patch, MagicMock, Mock

from tests.utils import IsolatedEnvTestCase, MockedBBTestCase
from bb_wrapper.wrapper.bb import BaseBBWrapper


class BaseBBWrapperTestCase(IsolatedEnvTestCase, MockedBBTestCase):
    def test_authenticate(self):
        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            401, data={"access_token": "access_token1", "token_type": "token_type"}
        )
        with patch('bb_wrapper.wrapper.bb.BaseBBWrapper.time.time') as mocked_time:
            mocked_time.return_value = 1
        result = BaseBBWrapper()._BaseBBWrapper__authenticate()

        self.assertEqual(result, True)

        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            401, data={"access_token": "access_token2", "token_type": "token_type"}
        )

        result = BaseBBWrapper()._BaseBBWrapper__authenticate(force=True)

        self.assertEqual(BaseBBWrapper().data.access_token, 'access_token2')

from unittest import TestCase
from utils.token import Token

class TestUnit(TestCase):
    def test_token_required(self):
        mock_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoxLCJpbWFnZVByb2ZpbGUiOiJpbWFnZS5wbmciLCJmaXJzdG5hbWUiOiJcdTBlMTVcdTBlMzhcdTBlMjVcdTBlMjJcdTBlMjdcdTBlMzFcdTBlMTUiLCJsYXN0bmFtZSI6Ilx1MGUxN1x1MGUzMVx1MGUxYVx1MGUwNFx1MGUwNyIsImVtYWlsIjoidHVseWF3YXR0QGdtYWlsLmNvbSIsInJvbGUiOiJBRE1JTiIsImNhciI6bnVsbH0sImV4cCI6MTY1ODg2NDA0N30.YdOzkUq4UZtP9CCpzG8qXBSJIwjQunE5F7MxFINz3FY'
        actual_one = Token.token_required(mock_token)
        self.assertEqual('decorated', actual_one.__name__)

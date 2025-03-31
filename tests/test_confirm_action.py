import unittest
from functions.confirm_action_message import confirm_action_message

class TestConfirmAction(unittest.TestCase):
    def test_confirm_action_import(self):
        # This test will pass if the function is imported correctly
        self.assertIsNotNone(confirm_action_message)

if __name__ == '__main__':
    unittest.main()

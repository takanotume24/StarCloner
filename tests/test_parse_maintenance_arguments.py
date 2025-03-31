import unittest
from functions.parse_arguments import parse_arguments
from unittest.mock import patch
import sys

class TestParseMaintenanceArguments(unittest.TestCase):
    def test_maintenance_move_temp_files(self):
        test_args = [
            "starcloner.py",
            "maintenance",
            "move-temp-files",
            "--dry-run"
        ]
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "maintenance")
            self.assertEqual(args.maintenance_command, "move-temp-files")
            self.assertTrue(args.dry_run)

if __name__ == "__main__":
    unittest.main()

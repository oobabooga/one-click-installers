# Author: Daethyra (Daemon Carino)
# Description: Unit tests for check_for_updates.py
import unittest
from unittest import mock
from check_for_updates import get_changed_files, update_files
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log to file
file_handler = logging.FileHandler('check_for_updates_test.log')
file_handler.setLevel(logging.INFO)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set format
formatter = logging.Formatter('%(levelname)s: %(message)s')
# Set format for handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class TestCheckForUpdates(unittest.TestCase):

    @mock.patch('check_for_updates.subprocess.run')
    @mock.patch('check_for_updates.subprocess.getoutput')
    def test_get_changed_files(self, mock_getoutput, mock_run):
        logger.info("Testing get_changed_files with mock data.")
        mock_getoutput.return_value = "start\nupdate\nrandomfile"
        mock_run.return_value = None
        files_to_check = ['start', 'update']
        
        result = get_changed_files(files_to_check)
        
        self.assertEqual(result, ['start', 'update'])
        logger.info("get_changed_files test passed.")

    @mock.patch('check_for_updates.subprocess.run')
    @mock.patch('check_for_updates.logging.info')
    @mock.patch('check_for_updates.logging.error')
    def test_update_files(self, mock_error, mock_info, mock_run):
        logger.info("Testing update_files with mock data.")
        mock_run.return_value = None
        changed_files = ['start', 'update']
        
        update_files(changed_files)
        
        mock_info.assert_called_with('Successfully updated update')
        logger.info("update_files test passed.")

    @mock.patch('check_for_updates.subprocess.run')
    @mock.patch('check_for_updates.logging.error')
    def test_get_changed_files_error(self, mock_error, mock_run):
        mock_run.side_effect = Exception('Failed')
        
        result = get_changed_files(['start', 'update'])
        
        mock_error.assert_called_with('Failed to get changed files: Failed')
        self.assertIsNone(result)
        logger.info("get_changed_files error test passed.")

    @mock.patch('check_for_updates.subprocess.run')
    @mock.patch('check_for_updates.logging.error')
    def test_update_files_error(self, mock_error, mock_run):
        mock_run.side_effect = Exception('Failed')
        
        update_files(['start'])
        
        mock_error.assert_called_with('Failed to update start: Failed')
        logger.info("update_files error test passed.")

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from personal_manager.core.config import (
    is_safe_to_delete_dir,
    find_paths_in_config,
    reset_application,
    is_path_inside_home
)

class TestConfigReset(unittest.TestCase):
    def setUp(self) -> None:
        """Create a temporary directory for file sandboxing."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
    def tearDown(self) -> None:
        """Clean up the sandbox directory."""
        if self.test_path.exists():
            shutil.rmtree(self.test_dir)

    def test_is_safe_to_delete_dir(self) -> None:
        """Test directory safety boundaries."""
        # System root and home folder should be unsafe
        self.assertFalse(is_safe_to_delete_dir(Path("/")))
        self.assertFalse(is_safe_to_delete_dir(Path.home()))
        
        # Standard system folders (if they exist) should be unsafe
        for d in ["/usr", "/var", "/etc", "/home"]:
            p = Path(d)
            if p.exists():
                self.assertFalse(is_safe_to_delete_dir(p))
                
        # A parent of home directory should be unsafe
        self.assertFalse(is_safe_to_delete_dir(Path.home().parent))
        
        # A sandboxed test directory should be safe
        sub_dir = self.test_path / "safe_dir"
        sub_dir.mkdir()
        self.assertTrue(is_safe_to_delete_dir(sub_dir))

    def test_is_path_inside_home(self) -> None:
        """Test home directory prefix constraint checks."""
        # Home directory itself should be True
        self.assertTrue(is_path_inside_home(Path.home()))
        
        # A subpath inside home should be True
        sub_dir = Path.home() / ".personal_manager"
        self.assertTrue(is_path_inside_home(sub_dir))
        
        # Root directory `/` should be False
        self.assertFalse(is_path_inside_home(Path("/")))
        
        # A subpath outside home (e.g. `/tmp` or `/usr`) should be False
        for d in ["/tmp", "/usr", "/var"]:
            p = Path(d)
            if p.exists() and p.resolve() != Path.home().resolve():
                self.assertFalse(is_path_inside_home(p))

    def test_find_paths_in_config(self) -> None:
        """Test recursive discovery of configured paths from TOML data."""
        # Create directories and files in the sandbox
        sub_dir = self.test_path / "logs"
        sub_dir.mkdir()
        temp_file = self.test_path / "budget.csv"
        temp_file.touch()
        
        config = {
            "project": {
                "name": "personal-manager",
                "version": "0.0.1"
            },
            "plugins": {
                "budgeting": True
            },
            "paths": {
                "log_dir": str(sub_dir.resolve())
            },
            "budgeting": {
                "expenses_file_path": str(temp_file.resolve())
            }
        }
        
        found_files, found_dirs = find_paths_in_config(config)
        
        # Verify correct extraction of files and directories
        self.assertIn(temp_file.resolve(), found_files)
        self.assertIn(sub_dir.resolve(), found_dirs)
        
        # None of the flat config string keys should be mistaken for files
        self.assertNotIn(Path("personal-manager").resolve(), found_files)

    @patch('personal_manager.core.config.load_config')
    @patch('builtins.input', return_value='y')
    def test_reset_application(self, mock_input: MagicMock, mock_load_config: MagicMock) -> None:
        """Test reset execution, ensuring deletions occur and empty parent is removed."""
        # Create temp config files inside sandbox
        config_parent = self.test_path / ".personal_manager"
        config_parent.mkdir()
        config_file = config_parent / "personal_manager.toml"
        config_file.touch()
        
        # Relocate the active CONFIG_FILE to our temp file
        import personal_manager.core.config
        old_config_file = personal_manager.core.config.CONFIG_FILE
        personal_manager.core.config.CONFIG_FILE = config_file
        
        # Create temp log and database files
        sub_dir = self.test_path / "logs"
        sub_dir.mkdir()
        temp_file = self.test_path / "budget.csv"
        temp_file.touch()
        
        mock_load_config.return_value = {
            "paths": {
                "log_dir": str(sub_dir.resolve())
            },
            "budgeting": {
                "expenses_file_path": str(temp_file.resolve())
            }
        }
        
        try:
            # Call reset
            reset_application()
            
            # Verify files are deleted
            self.assertFalse(temp_file.exists())
            self.assertFalse(sub_dir.exists())
            self.assertFalse(config_file.exists())
            self.assertFalse(config_parent.exists())  # Empty parent folder should be removed
        finally:
            # Restore original CONFIG_FILE path
            personal_manager.core.config.CONFIG_FILE = old_config_file

if __name__ == '__main__':
    unittest.main()

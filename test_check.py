import pytest
import subprocess
import sys
from check import get_scan_path


class TestChecker:
    """Minimal test suite for the challenge requirements checker"""

    def test_get_scan_path(self):
        """Test get_scan_path function"""
        assert get_scan_path() == "."
        assert get_scan_path("test") == "test"

    def test_monorepo_mode(self):
        """Test monorepo mode finds multiple challenges"""
        result = subprocess.run([
            sys.executable, "check.py", "--path", "test", "--monorepo"
        ], capture_output=True, text=True)
        
        assert "test/crypto/MrRobot" in result.stdout
        assert "test/web/flag-vault-1" in result.stdout

    def test_single_challenge_mode(self):
        """Test single challenge mode"""
        result = subprocess.run([
            sys.executable, "check.py", "--path", "test/web/flag-vault-1", "--single-challenge"
        ], capture_output=True, text=True)
        
        assert "test/web/flag-vault-1" in result.stdout
        assert result.returncode == 0


if __name__ == "__main__":
    pytest.main([__file__])
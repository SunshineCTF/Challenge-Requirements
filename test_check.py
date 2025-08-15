import pytest
import os
import glob
from check import Checker, get_scan_path


class TestChecker:
    """Test suite for the challenge requirements checker"""

    def get_rules(self):
        """Returns the standard rules for testing"""
        return [
            {
                "name": "Challenge Must Have a flag.txt",
                "file": "flag.txt",
                "description": "Contains the challenge's flag",
            },
            {
                "name": "Challenge must have a description.md",
                "file": "description.md",
                "description": "Contains the flavortext description to be presented to challengers",
                "markdown": True,
            },
            {
                "name": "Challenge must have a README.md",
                "file": "README.md",
                "description": "Contains detailed information about how to build and deploy the challenge",
                "markdown": True,
            },
            {
                "name": "Challenge can optionally have a solve.sh script",
                "file": "solve.sh",
                "description": "Contains a script that can validate that the challenge works as intended",
                "optional": True,
            },
        ]

    def test_get_scan_path_default(self):
        """Test get_scan_path with default value"""
        assert get_scan_path() == "."

    def test_get_scan_path_custom(self):
        """Test get_scan_path with custom path"""
        assert get_scan_path("test") == "test"

    def test_scan_test_directory(self):
        """Test scanning the test/ directory for challenges"""
        scan_path = get_scan_path("test")
        potential_challenges = glob.glob(f"{scan_path}/*/*")

        # Should find at least our test challenges
        assert len(potential_challenges) >= 2
        assert "test/crypto/MrRobot" in potential_challenges
        assert "test/web/flag-vault-1" in potential_challenges

    def test_crypto_mrrobot_challenge(self):
        """Test the crypto/MrRobot challenge (should fail - missing flag.txt)"""
        rules = self.get_rules()
        checker = Checker(rules, "test/crypto/MrRobot")
        result = checker.evaluate()

        assert result["challenge"] == "test/crypto/MrRobot"

        # Check individual rule results
        rule_results = {r["rule"]["file"]: r["result"] for r in result["rule_results"]}

        # Should fail flag.txt requirement
        assert rule_results["flag.txt"] == False
        # Should pass description.md and README.md
        assert rule_results["description.md"] == True
        assert rule_results["README.md"] == True

    def test_web_flag_vault_1_challenge(self):
        """Test the web/flag-vault-1 challenge (should pass most requirements)"""
        rules = self.get_rules()
        checker = Checker(rules, "test/web/flag-vault-1")
        result = checker.evaluate()

        assert result["challenge"] == "test/web/flag-vault-1"

        # Check individual rule results
        rule_results = {r["rule"]["file"]: r["result"] for r in result["rule_results"]}

        # Should pass all required files
        assert rule_results["flag.txt"] == True
        assert rule_results["description.md"] == True
        assert rule_results["README.md"] == True

    def test_nonexistent_challenge(self):
        """Test a nonexistent challenge directory"""
        rules = self.get_rules()
        checker = Checker(rules, "test/nonexistent/challenge")
        result = checker.evaluate()

        # All file checks should fail
        for rule_result in result["rule_results"]:
            if rule_result["rule"].get("file"):
                assert rule_result["result"] == False
    
    def test_monorepo_mode_flag(self):
        """Test that monorepo mode works with CLI arguments"""
        import subprocess
        import sys
        
        # Test monorepo mode (should find multiple challenges)
        result = subprocess.run([
            sys.executable, "check.py", "--path", "test", "--monorepo"
        ], capture_output=True, text=True)
        
        # Should find both challenges
        assert "test/crypto/MrRobot" in result.stdout
        assert "test/web/flag-vault-1" in result.stdout
    
    def test_single_challenge_mode_flag(self):
        """Test that single challenge mode works with CLI arguments"""
        import subprocess
        import sys
        
        # Test single challenge mode on flag-vault-1
        result = subprocess.run([
            sys.executable, "check.py", "--path", "test/web/flag-vault-1", "--single-challenge"
        ], capture_output=True, text=True)
        
        # Should only find the single challenge at the root path
        assert "test/web/flag-vault-1" in result.stdout
        # Should not contain subdirectory references
        assert "test/web/flag-vault-1/" not in result.stdout.replace("test/web/flag-vault-1", "")


if __name__ == "__main__":
    pytest.main([__file__])


.PHONY: test test-all test-crypto-mrrobot test-web-flag-vault-1 test-pytest test-act test-act-monorepo test-act-single test-act-validation help

# Default target
help:
	@echo "Available targets:"
	@echo "  test              - Run pytest test suite"
	@echo "  test-pytest       - Same as test"
	@echo "  test-all          - Run checker on test/ directory (all challenges)"
	@echo "  test-crypto-mrrobot - Run checker on test/crypto/MrRobot"
	@echo "  test-web-flag-vault-1 - Run checker on test/web/flag-vault-1"
	@echo "  test-act          - Run all act tests"
	@echo "  test-act-monorepo - Test monorepo mode with act"
	@echo "  test-act-single   - Test single challenge mode with act"
	@echo "  test-act-validation - Test validation logic with act"
	@echo "  help              - Show this help message"

# Default test target now runs pytest
test: test-pytest

test-pytest:
	@echo "Running pytest test suite..."
	pytest test_check.py -v

# Manual testing with the checker
test-all:
	@echo "Testing all challenges in test/ directory..."
	python3 check.py --path test

# Test individual challenges
test-crypto-mrrobot:
	@echo "Testing crypto/MrRobot challenge..."
	python3 check.py --path test/crypto/MrRobot

test-web-flag-vault-1:
	@echo "Testing web/flag-vault-1 challenge..."
	python3 check.py --path test/web/flag-vault-1

# Act tests for GitHub Actions
test-act: test-act-validation test-act-monorepo test-act-single

test-act-monorepo:
	@echo "Testing monorepo mode with act..."
	act -W .github/workflows/test-monorepo.yml

test-act-single:
	@echo "Testing single challenge mode with act..."
	act -W .github/workflows/test-single-challenge.yml

test-act-validation:
	@echo "Testing validation logic with act..."
	act -W .github/workflows/test-validation.yml
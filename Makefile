.PHONY: test test-monorepo test-single test-act help

# Default target
help:
	@echo "Available targets:"
	@echo "  test              - Run pytest test suite"
	@echo "  test-monorepo     - Test monorepo mode"
	@echo "  test-single       - Test single challenge mode"
	@echo "  test-act          - Test GitHub Actions with act"
	@echo "  help              - Show this help message"

# Default test target runs pytest
test:
	@echo "Running pytest test suite..."
	pytest test_check.py -v

# Test modes
test-monorepo:
	@echo "Testing monorepo mode..."
	python3 check.py --path test --monorepo

test-single:
	@echo "Testing single challenge mode..."
	python3 check.py --path test/web/flag-vault-1 --single-challenge

# Test with act
test-act:
	@echo "Testing GitHub Actions with act..."
	act -W .github/workflows/test-validation.yml
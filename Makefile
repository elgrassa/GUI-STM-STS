.PHONY: fmt lint test audit-deps scan-secrets security

fmt:
	ruff format .

lint:
	ruff check .

test:
	pytest

audit-deps:
	pip-audit -r requirements.txt

scan-secrets:
	gitleaks detect --source . --config .gitleaks.toml --redact --no-banner

security: audit-deps scan-secrets

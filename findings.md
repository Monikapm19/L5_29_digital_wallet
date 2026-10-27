# Lab 5: Static Code Analysis Findings

## Initial Analysis

### Pylint
- Initial score: 5.69/10
- Issues: Missing module and function docstrings, inconsistent naming, mutable default argument, global statement, and unused argument.

### Bandit

| Issue | Type | Line | Description | Fix Approach |
|---|---|---:|---|---|
| B105 | Security | 6 | Hardcoded gateway secret | Read secret from an environment variable |
| B324 | Security | 14 | Weak SHA-1 hash for PIN | Use a suitable salted PIN-hashing approach |
| B306 | Security | 60 | Insecure tempfile.mktemp() | Use a safe temporary-file creation method |
| B311 | Security | 64 | Non-cryptographic random OTP | Use the secrets module |

### Flake8

| Issue | Type | Line | Description | Fix Approach |
|---|---|---:|---|---|
| E261 | Style | 76 | Insufficient spacing before inline comment | Add the required spacing |
| E225 | Style | 78 | Missing whitespace around operator | Add whitespace |
| E231 | Style | 79 | Missing whitespace after comma | Add whitespace |
| E305 | Style | 80 | Missing blank lines after function definition | Add the required blank lines |

## Fix Verification
- Pylint target: Above 9.5/10
- Bandit: Address all reported findings
- Flake8: Resolve all reported formatting issues
- Save before-and-after reports for all three tools
- Create three commits documenting the fixes

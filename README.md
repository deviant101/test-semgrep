# SAST Demo App with Semgrep

This is a simple Python Flask application with **intentional security vulnerabilities** for testing Static Application Security Testing (SAST) using Semgrep in a GitHub Actions pipeline.

## ⚠️ Warning

This application contains **intentional security vulnerabilities** for educational and testing purposes only. **DO NOT deploy this application in production!**

## Intentional Vulnerabilities

The app includes the following vulnerabilities that Semgrep should detect:

1. **SQL Injection** - User input directly concatenated into SQL query
2. **Command Injection** - User input passed to shell command
3. **Cross-Site Scripting (XSS)** - User input rendered in template without escaping
4. **Hardcoded Secrets** - API keys and passwords in source code
5. **Insecure Deserialization** - Using pickle.loads on user input
6. **Debug Mode in Production** - Flask debug mode enabled

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── sast.yml          # GitHub Actions workflow for Semgrep
├── app.py                     # Flask application with vulnerabilities
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## GitHub Actions Pipeline

The pipeline (`.github/workflows/sast.yml`) will:

1. **Checkout** the repository code
2. **Set up Python** 3.11
3. **Install Semgrep** CLI tool
4. **Run Semgrep scan** with multiple rulesets:
   - `auto` - Automatic language detection
   - `p/security-audit` - Security-focused rules
   - `p/python` - Python-specific rules
5. **Display results** in the workflow logs
6. **Upload artifacts** (JSON and text reports)
7. **Upload SARIF** to GitHub Security tab (if available)

## Running Locally

### Install dependencies
```bash
pip install -r requirements.txt
pip install semgrep
```

### Run the app (for testing only)
```bash
python app.py
```

### Run Semgrep locally
```bash
# Basic scan
semgrep scan --config auto .

# Full security scan with output files
semgrep scan --config auto --config p/security-audit --config p/python --json --output results.json .
```

## Expected Semgrep Findings

When you run the pipeline, Semgrep should detect vulnerabilities like:
- `python.lang.security.audit.dangerous-subprocess-use`
- `python.flask.security.injection.sql-injection`
- `python.flask.security.injection.xss`
- `python.lang.security.deserialization.avoid-pickle`
- `generic.secrets.security.detected-generic-api-key`

## Usage

1. Push this code to a GitHub repository
2. The workflow will automatically run on push/PR to main/master
3. Check the "Actions" tab for results
4. Download artifacts from the workflow run
5. View security alerts in the "Security" tab (if SARIF upload succeeds)

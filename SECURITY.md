# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities in Arkival seriously.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send a report to the maintainers privately. Include:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

### Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a detailed response within 7 days indicating next steps
- We will work on a fix and coordinate disclosure timeline with you

### Security Best Practices

When using this system:

1. **API Keys**: Never commit API keys or sensitive credentials to version control
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **File Permissions**: Ensure proper file permissions on system files
4. **Updates**: Keep the system updated to the latest version
5. **Validation**: Validate all inputs and outputs in your workflows

### Safe Usage Guidelines

- Run the system in isolated environments when possible
- Regularly update dependencies
- Monitor system logs for unusual activity
- Use the built-in validation features
- Follow the principle of least privilege

Thank you for helping keep Arkival secure!

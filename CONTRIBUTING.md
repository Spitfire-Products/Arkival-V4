# Contributing to Arkival

Thank you for your interest in contributing! Arkival enables seamless knowledge transfer between AI agents and human developers across different development environments.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Run the setup script: `python3 setup_workflow_system.py`
4. Test your changes with: `python3 validate_deployment.py`

## Development Process

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/spitfire-products/arkival.git
cd arkival

# Run the setup
python3 setup_workflow_system.py

# Validate the setup
python3 validate_deployment.py
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Validate the setup: `python3 validate_deployment.py`
5. Update documentation as needed
6. Commit your changes with clear messages

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include breadcrumb documentation using `@codebase-summary:` format

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Test across different IDE environments when possible

### Documentation

- Update README.md if needed
- Add or update docstrings
- Include examples for new features
- Update CHANGELOG.md following semantic versioning

## Submitting Changes

1. Push your branch to your fork
2. Submit a pull request
3. Describe your changes clearly
4. Link any related issues

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment for all contributors

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Check existing issues before creating new ones

Thank you for contributing to making AI agent workflows more efficient!

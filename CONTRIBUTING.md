# Contributing to FinOps Agent Suite

Thank you for your interest in contributing to the FinOps Agent Suite! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12
- Azure subscription with Resource Graph access
- Azure OpenAI service deployed
- Service principal with appropriate permissions

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/finops-agent.git
   cd finops-agent
   ```

2. **Set up Environment**
   ```bash
   uv sync
   source .venv/bin/activate  # Linux/Mac
   # or on Windows: .venv\Scripts\activate
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

4. **Test Installation**
   ```bash
   python finops_cli.py status
   ./demo.sh
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add comprehensive docstrings
- Keep functions focused and small
- Use meaningful variable names

### Testing

- Test all new features with the demo script
- Ensure CLI commands work correctly
- Test error handling scenarios
- Verify Azure API integrations

### Documentation

- Update README.md for new features
- Add examples to PROJECT_DOCUMENTATION.md
- Include docstrings for all functions
- Update CLI help text

## 📋 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Implement your feature
   - Add tests
   - Update documentation
   - Test thoroughly

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

### PR Requirements

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Demo script works
- [ ] No sensitive data in commits
- [ ] Clear commit messages

## 🎯 Areas for Contribution

### High Priority
- **Cost Forecasting**: Add trend analysis and predictions
- **Multi-Subscription Support**: Scale to enterprise environments
- **Interactive Chat**: Add conversational AI interface
- **Automated Optimization**: Implement safe optimizations

### Medium Priority
- **Additional Azure Services**: Support more resource types
- **Cost Anomaly Detection**: ML-based anomaly detection
- **Report Templates**: Customizable report formats
- **API Endpoints**: REST API for integration

### Low Priority
- **UI Dashboard**: Web interface for the tool
- **Mobile App**: Mobile companion app
- **Plugin System**: Extensible architecture
- **Multi-Cloud Support**: AWS, GCP integration

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Details**
   - Python version
   - Operating system
   - Azure subscription type

2. **Steps to Reproduce**
   - Exact commands run
   - Expected vs actual behavior
   - Error messages

3. **Additional Context**
   - Screenshots if applicable
   - Log files
   - Configuration details

## 💡 Feature Requests

For feature requests, please:

1. **Check Existing Issues** - Avoid duplicates
2. **Describe Use Case** - Why is this needed?
3. **Provide Examples** - How would it work?
4. **Consider Implementation** - Any technical thoughts?

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Documentation**: Check PROJECT_DOCUMENTATION.md first

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FinOps Agent Suite! 🚀

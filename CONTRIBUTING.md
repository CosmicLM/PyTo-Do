# Contributing to PyTo-Do ✨

Thank you for your interest in contributing to PyTo-Do! We welcome contributions from everyone.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- A GitHub account

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PyTo-Do.git
   cd PyTo-Do
   ```
3. **Test the application:**
   ```bash
   python main.py
   ```

## 📝 How to Contribute

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce the bug
- Mention your Python version and OS

### 💡 Feature Requests
- Check existing issues first
- Describe the feature and its use case
- Consider contributing the implementation!

### 🔧 Code Contributions

#### Priority Areas (Help Wanted!)
- **Packaging**: Create `.exe` and `.deb` installers
- **GUI Development**: Build a graphical interface
- **Cloud Integration**: Google Tasks, Dropbox sync
- **Testing**: Add unit tests and integration tests
- **Documentation**: Improve code comments and guides

#### Making Changes
1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes**
3. **Test your changes thoroughly**
4. **Commit with descriptive messages:**
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push and create a Pull Request**

## 📋 Code Style Guidelines

### Python Code Style
- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use 4 spaces for indentation

### Project Structure
```
PyTo-Do/
├── main.py              # Main entry point
├── backend/
│   ├── main-cli.py      # CLI application
│   └── pytodo/          # Core modules
│       ├── tasks.py     # Task management
│       └── storage_processor.py  # File I/O
├── frontend/            # Future GUI components
└── assets/              # Images and resources
```

## 🧪 Testing

Before submitting:
- Test all existing functionality
- Test your new features
- Ensure the app works on Windows, macOS, and Linux (if possible)

## 📚 Documentation

When adding features:
- Update README.md if needed
- Add docstrings to new functions
- Include usage examples for new features

## 🎉 Pull Request Process

1. **Fork and create a feature branch**
2. **Make your changes**
3. **Write/update tests if applicable**
4. **Update documentation**
5. **Submit a Pull Request with:**
   - Clear title and description
   - Reference related issues
   - Screenshots (for UI changes)

## 📞 Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🎉**

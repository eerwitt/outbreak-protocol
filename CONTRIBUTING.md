# Contributing to Playtestr

Thank you for considering contributing to *Playtestr*! We welcome contributions that help improve the codebase, documentation, and features of this project. Please read this document to get started and ensure that your contributions meet our guidelines.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Code of Conduct](#code-of-conduct)
3. [How to Contribute](#how-to-contribute)
   - [Reporting Issues](#reporting-issues)
   - [Submitting Changes](#submitting-changes)
   - [Pull Request Process](#pull-request-process)
4. [Development Guidelines](#development-guidelines)
   - [Code Style](#code-style)
   - [Testing](#testing)
   - [Documentation](#documentation)
5. [Community](#community)

---

## Getting Started

1. **Fork the Repository:** Start by forking the *Playtestr* repository to your GitHub account.
2. **Clone Your Fork:** Clone the forked repository to your local development environment.
   ```bash
   git clone https://github.com/your-username/playtestr.git
   cd playtestr
   ```
3. **Set Up the Environment:** Follow the setup instructions in the README to configure your development environment. Make sure Docker and Docker Compose are installed, as *Playtestr* runs on a Docker-based setup.
4. **Create a Branch:** Before making any changes, create a new branch based on the feature or bug you plan to work on.
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code of Conduct

Please read and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). This project follows standards to ensure a respectful and inclusive community.

## How to Contribute

### Reporting Issues

If you find a bug, inconsistency, or something unclear in *Playtestr*, please [open an issue](https://github.com/lunchbreakgames/playtestr/issues). When reporting an issue, please be as descriptive as possible and include:
- A clear title
- Steps to reproduce the issue
- Expected vs. actual results
- Screenshots, if relevant
- The environment and version in which the issue occurred

### Submitting Changes

You can contribute in several ways, including:
1. **Bug Fixes**: Help us identify and resolve bugs in the project.
2. **Feature Requests**: Suggest new features or improvements.
3. **Documentation**: Improve or clarify the documentation.
4. **Tests**: Add or improve tests for existing code.

### Pull Request Process

1. **Make Your Changes**: Make changes in your branch. Try to keep each pull request focused on a single issue or feature.
2. **Commit Messages**: Write clear and descriptive commit messages. Use the following format:
   ```
   type(scope): description
   ```
   For example:
   ```
   feat(api): add endpoint for creating playtest schedules
   ```
3. **Push Your Branch**: Push your branch to GitHub.
   ```bash
   git push origin feature/your-feature-name
   ```
4. **Open a Pull Request**: Go to your fork on GitHub, and open a pull request to the `main` branch of the [Playtestr repository](https://github.com/lunchbreakgames/playtestr). Provide a description of your changes, linking to relevant issues if applicable.

5. **Request a Review**: Tag one of the project maintainers for a review of your pull request.

---

## Development Guidelines

### Code Style

- **Language**: *Playtestr* is primarily written in Python, so follow PEP 8 guidelines.
- **Consistency**: Keep code consistent with the existing codebase, including naming conventions, structure, and spacing.
- **Linting**: Run linters before submitting changes. We recommend using `flake8` for Python code.

### Testing

*Playtestr* relies on automated testing to ensure functionality remains stable. Follow these guidelines:
- **Write Tests**: All new code should include tests to cover functionality and edge cases.
- **Run Tests**: Run tests locally to verify that your changes do not break existing functionality.
   ```bash
   docker-compose -f docker-compose.test.yml up --build
   ```
- **Testing Framework**: We use `pytest` for Python tests. Write tests that are modular, clear, and maintainable.

### Documentation

Make sure any new features or changes are reflected in the documentation. This includes:
- **README.md**: Add or update usage instructions if your change affects installation or usage.
- **API Documentation**: Ensure that any new API endpoints, request parameters, or response fields are documented in the API section.
- **Comments**: Add inline comments for complex or critical sections of code to help future contributors understand your work.

## Community

For questions, discussions, and connecting with other contributors:
- **GitHub Discussions**: Use the [Discussions tab](https://github.com/lunchbreakgames/playtestr/discussions) for non-issue-related discussions and feedback.
- **Discord**: Join our Discord server [here](https://discord.gg/your-discord-invite) to chat with contributors and developers.

Thank you for contributing to *Playtestr*! Every contribution, no matter how big or small, is valuable to the community and helps make *Playtestr* a better tool for indie game developers.
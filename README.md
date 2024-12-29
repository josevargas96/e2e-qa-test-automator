# E2E QA Test Automator 🤖

An intelligent end-to-end testing automation framework that combines the power of AI with modern web testing tools. This project uses Python, Playwright, and Transformers to create a smart testing system that can autonomously explore and test web applications.

## Overview

This framework is designed to:
- Use AI to intelligently interact with web elements
- Automatically explore web applications
- Generate and execute test cases
- Create detailed reports of testing sessions

## Tech Stack
- **Python**: Core programming language
- **Playwright**: Modern web testing and automation
- **Transformers**: AI-powered decision making
- **HTML/CSS**: Test report generation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/josevargas96/e2e-qa-test-automator.git
cd e2e-qa-test-automator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
e2e-qa-test-automator/
├── src/                # Core source code
│   └── ...            # Source modules
├── tests/             # Test cases and scenarios
│   └── ...            # Test files
├── examples/          # Example usage and scenarios
│   └── ...            # Example files
├── config/            # Configuration files
│   └── ...            # Config files
├── main.py            # Main entry point
└── requirements.txt   # Python dependencies
```

## Configuration

1. Copy the example configuration file:
```bash
cp config/config.example.yaml config/config.yaml
```

2. Edit `config/config.yaml` with your settings:
- Browser settings (type, headless mode)
- Base URLs for testing
- AI model parameters
- Report generation preferences

## Usage

1. Basic usage:
```bash
python main.py --url https://example.com
```

2. Run with specific configuration:
```bash
python main.py --config custom_config.yaml
```

3. Generate detailed report:
```bash
python main.py --url https://example.com --report detailed
```

Check the `examples/` directory for more usage scenarios and sample test cases.

## Development

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt  # If available
```

4. Make your changes following our coding standards:
- Use PEP 8 style guide
- Add docstrings for functions and classes
- Include type hints
- Write unit tests for new features

5. Run tests:
```bash
pytest tests/
```

6. Submit a pull request

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Follow our development guidelines
4. Submit a pull request

## License

This project is open source and available under the MIT License.
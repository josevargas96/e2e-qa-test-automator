# E2E QA Test Automator 🤖

An intelligent end-to-end testing automation framework for web applications, combining AI-powered testing with data generation capabilities. Built with Python, Playwright, and modern testing tools.

## Tech Stack
- **Python**: Core programming language
- **Playwright**: Web testing and automation
- **Transformers**: AI-powered testing
- **Faker**: Test data generation
- **HTML/CSS**: Test reporting

## Prerequisites
- Python 3.8+
- pip
- Virtual environment

## Installation

```bash
# Clone repository
git clone https://github.com/josevargas96/e2e-qa-test-automator.git
cd e2e-qa-test-automator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install package in development mode
```

## Project Structure
```
e2e-qa-test-automator/
├── src/                  # Core source code
│   ├── ai_tester.py     # AI testing logic
│   ├── test_runner.py   # Test execution engine
│   └── utils/           # Utility modules
│       └── lead_data_generator.py  # Test data generation
├── tests/               # Test cases
├── examples/            # Usage examples
│   └── run_create_lead.py  # Lead creation example
├── config/              # Configuration
│   ├── test_cases/     # JSON test definitions
│   └── config.yaml     # Global config
└── requirements.txt     # Dependencies
```

## Usage Examples

### Create New Lead
```python
from src.test_runner import TestRunner
from src.utils.lead_data_generator import LeadDataGenerator

# Initialize
runner = TestRunner(config_path="config/config.json")
data_gen = LeadDataGenerator()

# Generate random lead data
lead_data = data_gen.generate_lead_data()

# Run test
runner.run_test(
    "config/test_cases/create_lead.json",
    variables=lead_data
)
```

### Run with Custom Config
```bash
python main.py --config custom_config.yaml
```

## Configuration

1. Copy example config:
```bash
cp config/config.example.yaml config/config.yaml
```

2. Configure in `config.yaml`:
```yaml
browser:
  type: chromium
  headless: false
  slowMo: 1000

baseUrl: https://example.com
```

## Development

1. Create feature branch:
```bash
git checkout -b feature/your-feature
```

2. Follow standards:
- PEP 8 style
- Type hints
- Docstrings
- Unit tests

3. Run tests:
```bash
pytest tests/
```

## Contributing
1. Fork repository
2. Create feature branch
3. Follow guidelines
4. Submit PR

## License
MIT License
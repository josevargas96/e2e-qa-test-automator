# E2E QA Test Automator 🤖

An intelligent end-to-end testing automation framework for web applications, combining AI-powered testing with data generation capabilities. Built with Python, Playwright, and modern testing tools.

## Features
- AI-powered testing automation
- Dynamic test data generation
- Configurable test execution
- Detailed test reporting
- URL logging with timestamps and user data
- Support for multiple test environments

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
- Local directory for test outputs

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
│   ├── run_create_lead.py           # Basic lead creation example
│   └── run_lead_with_address_data.py # Extended lead example
├── scripts/                # Utility scripts
│   └── setup_location_db.py  # Database initialization
├── config/              # Configuration
│   ├── test_cases/     # JSON test definitions
│   │   ├── create_lead.json             # Basic lead creation
│   │   └── create_lead_with_address_data.json  # Extended lead flow
│   └── data/               # Data storage
│       └── locations.db    # SQLite database for locations
│   └── config.yaml     # Global config
└── requirements.txt     # Dependencies
```

## Setup

### 1. Output Directory Setup
Create a local directory for test outputs:
```bash
# macOS/Linux
mkdir -p ~/Documents/test_outputs

# Windows
mkdir "%USERPROFILE%\Documents\test_outputs"
```

### 2. Get Absolute Path
```bash
# macOS/Linux
realpath ~/Documents/test_outputs

# Windows PowerShell
(Resolve-Path "$env:USERPROFILE\Documents\test_outputs").Path
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

# Add output directory configuration
output_dir: "/absolute/path/to/your/test_outputs"  # Use the path from step 2
```

## Location Data Management

### Initial Setup
1. Initialize the location database:
```bash
python scripts/setup_location_db.py
```
This creates a SQLite database with valid city, state, and ZIP code combinations for all 50 US states.

### Database Details
- Location: `config/data/locations.db`
- Contents: Valid city, state, and ZIP code combinations
- Coverage: Major cities from all 50 US states

### Lead Data Generation
The LeadDataGenerator now combines:
- Realistic street names (via Faker)
- Valid city, state, and ZIP combinations (via SQLite)

## Usage Examples

```python
from src.utils.lead_data_generator import LeadDataGenerator

# Initialize generator
data_gen = LeadDataGenerator()

# Generate lead data with valid address
lead_data = data_gen.generate_lead_data()
```

Generated data includes:
- First and last names
- Email and phone
- Complete address with:
  - Realistic street name
  - Valid city, state, ZIP combination


### Create New Lead with URL Logging
```python
from src.test_runner import TestRunner
from src.utils.lead_data_generator import LeadDataGenerator

# Initialize with configuration
config = {
    "headless": False,
    "slowMo": 1000,
    "output_dir": "/absolute/path/to/your/test_outputs"  # Your local path
}

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

### Test Case with URL Logging
```json
{
    "name": "Create Lead Test",
    "steps": [
        // ... other steps ...
        {
            "id": "capture_final_url",
            "action": "get_url",
            "description": "Capture and save final lead URL",
            "save_to_file": "lead_urls.txt"
        }
    ]
}
```

### Example Usage with Extended Data

```python
from src.test_runner import TestRunner
from src.utils.lead_data_generator import LeadDataGenerator

def main():
    # Initialize test runner
    config = {
        "headless": False,
        "slowMo": 1000,
        "output_dir": "/path/to/outputs"
    }
    runner = TestRunner(config_path="config/config.json")
    data_gen = LeadDataGenerator()

    # Generate lead data
    lead_variables = data_gen.generate_lead_data()
    
    # Run extended lead creation test
    runner.run_test(
        "config/test_cases/create_lead_with_address_data.json",
        variables=lead_variables,
        close_after=True
    )
```

### Output Format
The URL logging feature creates timestamped files with the following format:
```
lead_urls_20250103_143022.txt:
2025-01-03 14:30:22: John Smith - https://example.com/leads/12345
```

## Test Case Organization

### Naming Conventions
- Use descriptive, action-based names for test case files
- Include the primary functionality in the filename
- Examples:
  - `create_lead.json`
  - `create_lead_with_address_data.json`

### Test Case Structure
1. **Base Test Cases**
   - Focus on core functionality
   - Minimal dependencies
   - Example: `create_lead.json`

2. **Extended Test Cases**
   - Build upon base cases
   - Add additional functionality
   - Example: `create_lead_with_address_data.json`

### Complexity Management Guidelines
1. **Step Organization**
   - Group related steps together
   - Add descriptive comments
   - Include appropriate wait times

2. **Data Management**
   - Use the LeadDataGenerator for consistent data
   - Consider data dependencies
   - Handle required vs. optional fields

3. **Maintainability**
   - Keep test cases focused
   - Document complex selectors
   - Use clear step IDs and descriptions



### Run with Custom Config
```bash
python main.py --config custom_config.yaml
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

## Troubleshooting

### URL Logging Issues
1. Verify output directory exists and is writable
2. Check absolute path in configuration
3. Ensure test case includes "get_url" action
4. Check logs for any file permission issues

### Maintenance
- The database only needs to be created once
- Run setup script again to add more locations
- Uses UNIQUE constraints to prevent duplicates

## Contributing
1. Fork repository
2. Create feature branch
3. Follow guidelines
4. Submit PR

## License
MIT License
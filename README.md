# CIS Benchmark PDF Parser

## 🔍 Overview

A Python utility for transforming CIS (Center for Internet Security) Benchmark PDFs into structured, machine-readable CSV formats, addressing the limitation of PDFs being the sole distribution method.

## 🚀 Key Features

- 📄 PDF to CSV conversion
- 🔒 Comprehensive benchmark data extraction
- 🧩 Flexible parsing for various CIS benchmark documents

## 📋 Prerequisites

### System Requirements

- Python 3.8+
- pip package manager

### Dependencies

- PyMuPDF (fitz)
- csv
- re
- logging
- argparse

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/cis-benchmark-pdf-parser.git
cd cis-benchmark-pdf-parser
```

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🖥 Usage

### Basic Usage

```bash
python3 cis_pdf_parser.py --pdf_file <path_to_benchmark_pdf> --out_file <output_csv>
```

### Command-Line Options

```
$ python3 cis_pdf_parser.py --help
usage: cis_pdf_parser.py [-h] --pdf_file PDF_FILE --out_file OUT_FILE [-l LOG_LEVEL]

Parses CIS Benchmark PDF content into CSV Format

optional arguments:
  -h, --help            show this help message and exit
  --pdf_file PDF_FILE   PDF File to parse
  --out_file OUT_FILE   Output file in .csv format
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Set log level (DEBUG, INFO, etc). Default to INFO
```

### Example

```bash
python3 cis_pdf_parser.py \
    --pdf_file CIS_Red_Hat_Enterprise_Linux_7_Benchmark_v3.1.1.pdf \
    --out_file rhel_7_controls.csv
```

## 📊 Output Format

The parser extracts the following fields:

- Rule
- Profile Applicability
- Description
- Rationale
- Audit
- Remediation
- CIS Controls

## 🧪 Compatibility

**Tested Benchmark Versions:**

- CIS Oracle Linux 7 Benchmark v3.1.1
- CIS Red Hat Enterprise Linux 8 Benchmark v1.0.1
- CIS Red Hat Enterprise Linux 7 Benchmark v3.1.1

## 🎯 Use Cases

1. **Enhanced Security Assessment**

   - Augment security tool outputs with detailed benchmark information
   - Extract comprehensive control details not typically available

2. **Automation**

   - Automate PDF benchmark conversion
   - Integrate with security assessment workflows

3. **Data Interoperability**
   - Generate CSV files for further processing
   - Enable cross-platform benchmark analysis

## 🚧 Roadmap & TODO

### Immediate Improvements

- [ ] Implement robust error handling
- [ ] Expand PDF format support
- [ ] Develop comprehensive unit tests
- [ ] Create flexible configuration management

### Future Enhancements

- [ ] Multi-language PDF support
- [ ] Performance optimization
- [ ] Advanced logging mechanisms
- [ ] Docker containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 🔒 Security

For security issues, please refer to [CONTRIBUTING.md](CONTRIBUTING.md#security-issue-notifications)

## 📜 License

MIT-0 License. See [LICENSE](LICENSE) file for details.

## 👥 Contributors

### Original Authors

- David Bailey, [dbawssec@amazon.com](mailto:dbawssec@amazon.com)
- ThibautB, [thibon](https://github.com/thibon)

### Project Maintainers

- Natthawat B, [hx-natthawat](https://github.com/hx-natthawat)

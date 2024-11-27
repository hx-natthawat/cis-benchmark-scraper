# CIS Benchmark PDF Parser

## Overview

A Python utility to parse CIS (Center for Internet Security) Benchmark PDFs and convert their content into a structured CSV format. This tool helps security professionals and system administrators easily extract and analyze CIS benchmark rules.

## Features

- Supports multiple CIS Benchmark types:
  - Windows Server 2012/2019
  - Windows 10 Enterprise
  - Linux distributions (RHEL, CentOS, Ubuntu, Debian)
  - Apache Tomcat 8/10
- Extracts comprehensive rule information:
  - Rule number
  - Profile Applicability
  - Description
  - Rationale
  - Audit instructions
  - Remediation steps
  - Default values
  - CIS Controls

## Requirements

- Python 3.8+
- pymupdf
- Recommended: virtual environment

## Installation

1. Clone the repository
2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python cis_pdf_parser.py --pdf_file path/to/benchmark.pdf --out_file output.csv [--log-level INFO]
```

### Arguments

- `--pdf_file`: Path to the CIS Benchmark PDF (Required)
- `--out_file`: Path for the output CSV file (Required)
- `--log-level`: Logging level (Optional, default: INFO)

## Supported CIS Benchmark Types

- Apache Tomcat 8/10
- Red Hat Enterprise Linux 7
- Debian Linux 11
- CentOS Linux 7
- Ubuntu Linux 22.04
- Microsoft Windows Server 2012/2019
- Microsoft Windows 10 Enterprise

## Logging

The parser uses Python's logging module. Log levels include:

- DEBUG: Detailed diagnostic information
- INFO: General information about parsing progress
- WARNING: Potential issues that don't prevent parsing
- ERROR: Serious problems that might interrupt parsing

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the terms specified in the `LICENSE` file.

## Disclaimer

This tool is not officially affiliated with the Center for Internet Security. Always refer to the original CIS Benchmark documents for the most accurate and up-to-date information.

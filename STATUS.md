# Project Status and Error Handling Guide

## Current Status

- Project Version: 1.0.0
- Last Updated: [Current Date]
- Parsing Stability: Beta

## Supported CIS Benchmark Types

- [x] Apache Tomcat 8
- [x] Apache Tomcat 10
- [x] Red Hat Enterprise Linux 7
- [x] Debian Linux 11
- [x] CentOS Linux 7
- [x] Ubuntu Linux 22.04
- [x] Microsoft Windows Server 2012
- [x] Microsoft Windows Server 2019
- [x] Microsoft Windows 10 Enterprise

## Common Error Messages and Troubleshooting

### 1. PDF Parsing Errors

- **Error**: "Not a valid CIS PDF Benchmark"

  - **Cause**: PDF does not match expected structure
  - **Solution**:
    - Verify PDF is an official CIS Benchmark document
    - Check PDF is not corrupted
    - Ensure PDF is not password-protected

- **Error**: "Could not find CIS Name"
  - **Cause**: Unable to identify benchmark type from cover page
  - **Solution**:
    - Confirm PDF cover page contains "CIS" and "Benchmark"
    - Manually verify benchmark type matches supported list

### 2. Regex Matching Errors

- **Error**: "No matching regex for {benchmark_name}"
  - **Cause**: Benchmark type not in predefined patterns
  - **Solution**:
    - Check if benchmark is a newly released version
    - Open an issue on GitHub with PDF details
    - Consider contributing a new regex pattern

### 3. File and Permission Errors

- **Error**: Permission denied when writing output CSV
  - **Solution**:
    - Check write permissions in target directory
    - Run script with appropriate user privileges
    - Use absolute file paths

### 4. Dependency Errors

- **Error**: ModuleNotFoundError for pymupdf
  - **Solution**:
    - Reinstall dependencies: `pip install -r requirements.txt`
    - Verify Python version compatibility
    - Create a fresh virtual environment

## Logging Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General parsing progress
- **WARNING**: Potential parsing issues
- **ERROR**: Critical failures preventing parsing

## Recommended Debugging Steps

1. Run with `--log-level DEBUG` for detailed output
2. Verify input PDF integrity
3. Check Python and dependency versions
4. Validate file paths and permissions

## Reporting Issues

- Include full log output
- Provide sample PDF (if possible)
- Specify Python and dependency versions

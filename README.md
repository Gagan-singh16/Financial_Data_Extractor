# Financial Data Extractor

A Python tool that extracts tables and financial data from PDF financial reports and exports them to CSV or Excel format.

## Features

- Extract tables from PDF financial reports
- Support for both single PDF files and directories containing multiple PDFs
- Export extracted tables to CSV or Excel format
- Automatic cleaning of extracted data
- Handles multiple pages in PDF documents

## Installation

1. Make sure you have Python 3.7 or higher installed on your system.

2. Clone this repository or download the source code.

3. Install the required dependencies:

```bash
pip install pandas openpyxl pdfplumber
```

## Usage

### Basic Usage

To extract tables from a single PDF file:

```bash
python financial_data_extractor.py path/to/your/file.pdf
```

To extract tables from all PDF files in a directory:

```bash
python financial_data_extractor.py path/to/your/directory
```

### Advanced Options

- Specify output directory:

```bash
python financial_data_extractor.py input.pdf --output ./my_output_folder
```

- Choose output format (CSV or Excel):

```bash
python financial_data_extractor.py input.pdf --format excel
```

### Command Line Arguments

- `input`: Required. Path to the input PDF file or directory containing PDF files
- `--output` or `-o`: Optional. Output directory for extracted tables (default: ./output)
- `--format` or `-f`: Optional. Output format - either 'csv' or 'excel' (default: csv)

## Output

- For CSV output: Each table will be saved as a separate CSV file named `{original_filename}_table_{number}.csv`
- For Excel output: All tables from a PDF will be saved in a single Excel file named `{original_filename}_tables.xlsx`, with each table on a separate sheet

## Example

```bash
# Extract tables from a single PDF and save as CSV files
python financial_data_extractor.py financial_report.pdf

# Extract tables from all PDFs in a directory and save as Excel files
python financial_data_extractor.py ./reports_folder --format excel --output ./extracted_data
```

## Notes

- The tool automatically cleans the extracted data by:
  - Removing empty rows and columns
  - Converting numeric values to appropriate data types
  - Cleaning column names (removing newlines and extra spaces)
- If no tables are found in a PDF, a message will be displayed
- The output directory will be created automatically if it doesn't exist

## Requirements

- Python 3.7+
- pandas
- openpyxl
- pdfplumber

## License

This project is not open source. Meant for private use only

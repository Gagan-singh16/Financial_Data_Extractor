#!/usr/bin/env python3
# Financial Data Extractor
# Extracts tables and financial data from various financial reports and exports to CSV/Excel

import os
import argparse
import pandas as pd
import pdfplumber
import glob

class FinancialDataExtractor:
    """Extract tables and financial data from financial reports"""

    def __init__(self, input_path, output_path, output_format="csv"):
        """Initialize the extractor with input and output paths"""
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format.lower()
        
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_path, exist_ok=True)
    
    def process_files(self):
        """Process all financial reports in the input path"""
        if os.path.isdir(self.input_path):
            pdf_files = glob.glob(os.path.join(self.input_path, "*.pdf"))
            for pdf_file in pdf_files:
                self.extract_data_from_file(pdf_file)
        elif os.path.isfile(self.input_path) and self.input_path.lower().endswith('.pdf'):
            self.extract_data_from_file(self.input_path)
        else:
            print(f"Error: {self.input_path} is not a valid PDF file or directory")
    
    def extract_data_from_file(self, file_path):
        """Extract data from a single financial report"""
        print(f"Processing: {file_path}")
        
        tables = []
        
        # Use pdfplumber for table extraction
        try:
            print("Extracting tables with pdfplumber...")
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    print(f"Processing page {page_num}...")
                    extracted_tables = page.extract_tables()
                    for table in extracted_tables:
                        if table and len(table) > 0:
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append(df)
            print(f"Found {len(tables)} tables")
        except Exception as e:
            print(f"Error during extraction: {e}")
        
        # Save extracted tables
        if tables:
            self.save_tables(tables, file_path)
        else:
            print(f"No tables found in {file_path}")
    
    def save_tables(self, tables, file_path):
        """Save extracted tables to CSV or Excel"""
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        if self.output_format == "csv":
            for i, table in enumerate(tables):
                # Clean the table - remove empty rows and columns
                table = self.clean_table(table)
                
                # Skip empty tables
                if table.empty:
                    continue
                    
                output_file = os.path.join(self.output_path, f"{base_name}_table_{i+1}.csv")
                table.to_csv(output_file, index=False)
                print(f"Saved table {i+1} to {output_file}")
        else:  # Excel
            output_file = os.path.join(self.output_path, f"{base_name}_tables.xlsx")
            with pd.ExcelWriter(output_file) as writer:
                for i, table in enumerate(tables):
                    # Clean the table - remove empty rows and columns
                    table = self.clean_table(table)
                    
                    # Skip empty tables
                    if table.empty:
                        continue
                        
                    table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
            print(f"Saved all tables to {output_file}")
    
    def clean_table(self, df):
        """Clean the table by removing empty rows and columns and fixing data types"""
        if df is None or df.empty:
            return pd.DataFrame()
            
        # Try to convert numeric columns to float
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
                
        # Drop rows where all elements are NaN
        df = df.dropna(how='all')
        
        # Drop columns where all elements are NaN
        df = df.dropna(axis=1, how='all')
        
        # Clean column names - remove newlines and extra spaces
        df.columns = [str(col).strip().replace('\n', ' ').replace('  ', ' ') for col in df.columns]
        
        return df

def main():
    parser = argparse.ArgumentParser(description='Extract tables from financial reports')
    parser.add_argument('input', help='Input PDF file or directory containing PDF files')
    parser.add_argument('--output', '-o', default='./output', help='Output directory for extracted tables')
    parser.add_argument('--format', '-f', choices=['csv', 'excel'], default='csv', help='Output format (csv or excel)')
    
    args = parser.parse_args()
    
    extractor = FinancialDataExtractor(args.input, args.output, args.format)
    extractor.process_files()

if __name__ == "__main__":
    main() 
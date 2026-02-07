## This script takes the column from your excel sheet and parses it row by row to find out German words from the different rows and creates a list of them with the sample ids. 

## to run: python3 german_words.py <path_to_excel_file> <sample id column name> <German words containing column name> <path_to_output_file>

import pandas as pd
from langdetect import detect, DetectorFactory
import re
import sys

DetectorFactory.seed = 0

def is_german(text):
    try:
        return detect(text) == 'de'
    except:
        return False
    
def extract_german_words(text):
    # This regex will match words containing German characters
    german_words = re.findall(r'\b[\wäöüßÄÖÜ]+\b', text)
    return ",".join(german_words)

def parse_excel(file_path, sample_id_col, karyotype_col, output_file):
    print(24,sample_id_col, karyotype_col)
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Open the output file
    with open(output_file, 'w') as f:
        # Write the header
        f.write('Sample ID\tKaryotype\tGerman Words\n')

        # Iterate through the rows
        for index, row in df.iterrows():
            sample_id = row[sample_id_col]
            karyotype = row[karyotype_col]

            if is_german(karyotype):
                german_words = extract_german_words(karyotype)
                f.write(f'{sample_id}\t{karyotype}\t{german_words}\n')

if __name__ == "__main__":
    # Specify the file path and column names
    file_path = sys.argv[1]
    sample_id_col = str(sys.argv[2])  # Replace with your actual column name
    karyotype_col = str(sys.argv[3])  # Replace with your actual column name
    output_file = sys.argv[4]

    # Parse the Excel file and extract the required information
    parse_excel(file_path, sample_id_col, karyotype_col, output_file)
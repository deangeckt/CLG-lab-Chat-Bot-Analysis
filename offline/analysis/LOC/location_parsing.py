import pandas as pd
import openai
import os
from tqdm import tqdm
import json
import csv
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"


def load_orig_xlsx():
    # Load Excel file
    file_name = 'participants_4-21-25'
    sheet_ ='insertional only'   # 'alternation only'
    df = pd.read_excel(f"{file_name}.xlsx", sheet_name=sheet_)

    # Clean and prepare location strings
    df = df.fillna("")
    location_lines = []
    for _, row in df.iterrows():
        birth = row["Place of birth (state, country):"].strip()
        res = row["Place of current residence (approximate city, state, country):"].strip()
        line = f"Birth: {birth} || Residence: {res}"
        location_lines.append(line)
    print(len(location_lines))
    print()
    # Combine into single prompt
    joined_text = "\n".join(location_lines)
    print(joined_text)


"""
TO CLAUDE:
You are a structured data extraction assistant. Extract the US state (if any, or other countries) and 2-letter country code from each row of location data.

Each row has two fields: birth and residence, separated by ||.
Answer in a format separated by ||
e.g.: Birth || Residence || Birth State || Birth Country ||  Residence State || Residence Country

Some rows might be blank / missing; for these keep it blank.

respond in a text line by line so later i could parse it with python to a csv.
"""


def parse_location_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='',
                                                                 encoding='utf-8') as outfile:
        # Create CSV writer
        csv_writer = csv.writer(outfile)

        # Write header row
        csv_writer.writerow(['Birth Location', 'Residence Location', 'Birth State', 'Birth Country', 'Residence State',
                             'Residence Country'])

        # Process each line in the input file
        for line in infile:
            line = line.strip()
            if line:
                # Split the line by '||' delimiter and strip whitespace from each field
                fields = [field.strip() for field in line.split('||')]

                # Write the parsed data to CSV
                csv_writer.writerow(fields)

    print(f"Data successfully parsed and saved to {output_file}")


# Example usage
if __name__ == "__main__":
    # load_orig_xlsx()
    parse_location_data('ins_loc_claude.txt', 'ins_data.csv')

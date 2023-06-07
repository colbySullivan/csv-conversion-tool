# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os

def convert():
    csv_directory = 'csvFolder'

    # iterate over files in
    # that directory
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            f = os.path.join(csv_directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                df1 = pd.read_csv(f)
                html_file = df1.to_html()
                path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                print(f)
                buffer = f[:-3]
                pdf_file = buffer + "pdf"
                pdfkit.from_string(html_file, pdf_file, configuration=config)

def main():
    convert()
    
                               
if __name__ == "__main__":
    # execute only if run as a script
    main()
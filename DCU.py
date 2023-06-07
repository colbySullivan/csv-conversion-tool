# Data Conversion Utility Script

import pandas as pd
import pdfkit

def main():
    file = "testCSV.csv"
    df1 = pd.read_csv(file)
    print(df1)
    html_string = df1.to_html()
    pdfkit.from_string(html_string, "output_file.pdf")

if __name__ == "__main__":
    # execute only if run as a script
    main()
# import camelot
# from PyPDF2 import PdfFileReader
import PyPDF2
from tabula.io import read_pdf
import pandas as pd
# from typing import Dict, Union
#
# from pypdf import PdfReader



def read_file(filename):
    tables = read_pdf(filename, pages='all')
    records=tables[-1].to_dict('records')
    return records

def ocr_main(filename):
    try:
        tables_dict=read_file(filename)
        if 'Description' in tables_dict[0].keys():
            for i, row in enumerate(tables_dict):
                if pd.isna(row['No']) == True  and pd.isna(row['Amount']) == True:
                    tables_dict[i - 1].update({"Description": tables_dict[i - 1]['Description'] + " " + row['Description']})
                    # tables_dict.pop(i)
            df = pd.DataFrame.from_dict(tables_dict)
            df.rename(columns={"Price/Unit":"Price"}, inplace=True)
            # df = df.dropna(thresh=6)
            df = df.dropna(subset=["Amount"])
            df = df.fillna('')
            return df.to_dict('records')
        else:
            tables_dict1=[]
            UOM_list=["per cntr","per set","per shpt"]
            for i,row in enumerate(tables_dict):
                if pd.isna(row['No']) == True and pd.isna(row['Amount']) == True:
                    tables_dict1[i - 1].update({"Description UOM": tables_dict1[i - 1]['Description UOM'] + " " + row['Description UOM']})
                    tables_dict1.append(row)
                    continue
                for Uom_value in UOM_list:
                    if Uom_value in row['Description UOM']:
                        des_value=row['Description UOM'].replace(Uom_value,"").strip()
                        row.update({'Description UOM': des_value})
                        row['UOM']=Uom_value
                tables_dict1.append(row)
            # tables_dict
            df = pd.DataFrame.from_dict(tables_dict1)
            df.rename(columns={"Description UOM": "Description","Price/Unit":"Price"}, inplace=True)
            # df=df.dropna(thresh=6)
            df = df[["No", "Description", "UOM", "Cur", "Qty", "Price", "ROE", "Amount"]]
            df1 = df.dropna(subset=["Amount"])
            df1 = df1.fillna('')
            return df1.to_dict('records')
    except:
        try:
            from pdfquery import PDFQuery
            pdf = PDFQuery(filename)
            pdf.load()
            # from bs4 import BeautifulSoup
            data = pdf.extract([
                ('with_formatter', 'text'),
                ('Description', 'LTTextLineHorizontal:in_bbox("60.963, 357.153, 172.928, 369.369")'),
                ('UOM', 'LTTextLineHorizontal:in_bbox("240.0, 357.153, 270.34, 369.369")'),
                ('Cur', 'LTTextLineHorizontal:in_bbox("300.0, 357.153, 318.893, 369.369")'),
                ('Price', 'LTTextLineHorizontal:in_bbox("420.0, 357.153, 449.857, 369.369")'),
                ('No','LTTextLineHorizontal:in_bbox("30.0, 357.153, 37.464, 369.369")'),
                ('Qty', 'LTTextLineHorizontal:in_bbox("30.0, 357.153, 37.464, 369.369")'),
                ('ROE', 'LTTextLineHorizontal:in_bbox("53.25, 357.153, 60.963, 382.025")'),
                ('Amount', 'LTTextLineHorizontal:in_bbox("420.0, 357.153, 449.857, 369.369")'),
            ])
            return data
        except Exception as e:
            print(e)


if __name__ == '__main__':
    filename = "PLIV23002807.pdf"
    ocr_main(filename)


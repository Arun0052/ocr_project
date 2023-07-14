from tabula.io import read_pdf
import pandas as pd



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
    except Exception as e:
        print(e)
        return str(e)

if __name__ == '__main__':
    filename = "PLIV23002807.pdf"
    ocr_main(filename)


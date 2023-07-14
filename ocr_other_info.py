#importing required modules
import PyPDF2
import re


# creating a pdf file object
def read_invoice(file):
        info_dict={}
        try:
                pdfFileObj = open(file, 'rb')
                # creating a pdf reader object
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                pages=pdfReader.numPages
                # printing number of pages in pdf file
                for i in range(pages):
                        # Creating a page object
                        pageObj = pdfReader.getPage(i)
                        # Printing Page Number
                        if i==0:
                                texts = pageObj.extractText().split("\n")
                                for text in texts:
                                        if "Description:" in text:
                                                # print("description")
                                                info_dict['Description']=text.split(":")[-1].strip()
                                        elif "COVERIGHT SURFACES" in text:
                                                if re.match(r'\d{2}/\d{2}/\d{4}', text):
                                                        match_str=re.search(r'\d{2}/\d{2}/\d{4}', text)
                                                        info_dict['date']=match_str.group()
                                                        invoice=text.replace(match_str.group(),"")
                                                        info_dict['invoiceNo']=invoice.split(" ")[0].strip()
                                        elif "Account No:" in text:
                                                info_dict['AccounNo']=text.split(":")[-1].strip()
                                        elif "Beneficiary Name" in text:
                                                info_dict['Org_Name']=text.split(":")[-1].strip()
                return info_dict
                # closing the pdf file object
                pdfFileObj.close()
        except Exception as e:
                print(e)
                return info_dict

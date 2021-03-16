import pandas as pd 
  
 
def read_excel_sheets(xls_path):
    """Read all sheets of an Excel workbook and return a single DataFrame"""
    print(f'Loading {xls_path} into pandas')
    xl = pd.ExcelFile(xls_path)
    df = pd.DataFrame()
    columns = None
    dff = pd.DataFrame()
    for idx, name in enumerate(xl.sheet_names):
        print(f'Reading sheet #{idx}: {name}')
        sheet = xl.parse(name)
        if idx == 0:
            # Save column names from the first sheet to match for append
            columns = sheet.columns
        sheet.columns = columns
        # Assume index of existing data frame when appended
        #df = df.append(sheet, ignore_index=True)
        dfa  = pd.read_excel(xls_path , sheet_name=idx)
        print (dfa)
        dff = pd.concat([dff, dfa])
    return dff


# Read excel file 
# and store into a DataFrame 
df1 = read_excel_sheets('copyexcell1.xlsx') 
df2 = read_excel_sheets('copyexcell2.xlsx') 
print(df1) 
#print(df2)
# concat both DataFrame into a single DataFrame 
df = pd.concat([df1, df2]) 
  
# Export Dataframe into Excel file 
df.to_excel('final_output.xlsx', index=False)

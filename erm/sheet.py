import pandas as pd

# Define the path to the Excel file
excel_file = r'C:\Users\Mostafa\IAM-App\internal_audit_management\uploads\hwb_2015.xlsx'

# Read each sheet and store it in the dictionary

df = pd.read_excel(excel_file, sheet_name='Sales Data')

# Display the first 5 rows of each sheet
print(df.head(), "\n")
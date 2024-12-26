import pandas as pd
import datetime

# Load the pickle file
pickle_path = "sales_data.pkl"
sales_data = pd.read_pickle(pickle_path)

# Rename columns for consistency
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

# Define valid date range
current_date = datetime.datetime.now()
valid_start_date = pd.Timestamp("2015-01-01")  # Assuming the data starts in 2015
valid_end_date = current_date

# Identify rows with invalid dates
invalid_dates = sales_data[(sales_data['inv_date'] < valid_start_date) | (sales_data['inv_date'] > valid_end_date)]

# Display summary of invalid dates
print(f"Number of invalid invoice dates: {len(invalid_dates)}")
print(invalid_dates[['invoice', 'inv_date']].head())

# Save invalid dates to a CSV for further review (optional)
invalid_dates.to_csv("invalid_invoice_dates.csv", index=False)

# Visualize invalid dates
import plotly.express as px

# Aggregate invalid invoices by date
invalid_date_counts = invalid_dates['inv_date'].value_counts().reset_index()
invalid_date_counts.columns = ['inv_date', 'count']

# Sort by date
invalid_date_counts = invalid_date_counts.sort_values(by='inv_date')

# Create a line chart
fig_invalid_dates = px.line(
    invalid_date_counts,
    x='inv_date',
    y='count',
    title="Invalid Invoice Dates Over Time",
    labels={'inv_date': 'Invoice Date', 'count': 'Number of Invalid Entries'},
    markers=True
)

# Show the plot
fig_invalid_dates.show()

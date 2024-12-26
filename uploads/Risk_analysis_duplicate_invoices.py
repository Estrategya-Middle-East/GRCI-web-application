import pandas as pd

# # Load the Excel file and specify the sheet
# file_path = "Sales_2015.xlsx"
# sales_data = pd.read_excel(file_path, sheet_name="Sales Data")

# # Save as a pickle file
# pickle_path = "sales_data.pkl"
# sales_data.to_pickle(pickle_path)
pickle_path = r"C:\Users\Mostafa\IAM-App\internal_audit_management\uploads\sales_data.pkl"
# Load the pickle file
sales_data = pd.read_pickle(pickle_path)

# Confirm it loaded correctly
print(sales_data.head())
# Rename columns for easier access
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

import pandas as pd

# Count duplicates for each invoice
invoice_counts = sales_data['invoice'].value_counts()

# Filter only duplicates (more than 1 occurrence)
duplicate_invoice_counts = invoice_counts[invoice_counts > 1]

# Convert to DataFrame for plotting
duplicate_invoice_summary = duplicate_invoice_counts.reset_index()
duplicate_invoice_summary.columns = ['invoice', 'count']

# Display summary
print(duplicate_invoice_summary.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Limit to top 20 duplicate invoices for visualization
top_duplicates = duplicate_invoice_summary.head(20)

# Create a bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=top_duplicates, x='invoice', y='count', palette="viridis")

# Add labels and title
plt.title("Top 20 Duplicate Invoices", fontsize=16)
plt.xlabel("Invoice Number", fontsize=12)
plt.ylabel("Duplicate Count", fontsize=12)
plt.xticks(rotation=45)
plt.show()

import plotly.express as px

# Sort and select top 100 duplicate invoices
top_100_duplicates = duplicate_invoice_summary.sort_values(by='count', ascending=False).head(100)

# Convert 'invoice' to a string to ensure it's treated as a category
top_100_duplicates['invoice'] = top_100_duplicates['invoice'].astype(str)

# Create the bar plot
fig_bar = px.bar(
    top_100_duplicates,
    x='invoice', 
    y='count',
    title="Top 100 Duplicate Invoices",
    labels={'count': 'Duplicate Count', 'invoice': 'Invoice Number'},
    color='count',
    color_continuous_scale='Viridis',
    height=600
)

# Update x-axis settings
fig_bar.update_layout(
    xaxis=dict(title_text="Invoice Number", title_font_size=14, categoryorder="total descending", tickangle=45),
    yaxis=dict(title_text="Duplicate Count", title_font_size=14)
)

# Show the plot
fig_bar.show()



# Create a summary of unique vs duplicate invoices
total_entries = len(sales_data)
unique_invoices = len(invoice_counts[invoice_counts == 1])
duplicate_invoices = total_entries - unique_invoices

# Data for pie chart
pie_data = pd.DataFrame({
    "Type": ["Unique Invoices", "Duplicate Invoices"],
    "Count": [unique_invoices, duplicate_invoices]
})

# Create an interactive pie chart
fig_pie = px.pie(
    pie_data,
    values='Count',
    names='Type',
    title="Distribution of Duplicate vs Unique Invoices",
    color='Type',
    color_discrete_map={"Unique Invoices": "blue", "Duplicate Invoices": "orange"}
)

# Show the pie chart
fig_pie.show()
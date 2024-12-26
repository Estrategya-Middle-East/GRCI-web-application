import pandas as pd
import matplotlib.pyplot as plt

# Load the pickle file
pickle_path = r"C:\Users\Mostafa\IAM-App\internal_audit_management\uploads\sales_data.pkl"
sales_data = pd.read_pickle(pickle_path)

# Rename columns for consistency
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

# Identify positive and negative subtotals
positive_subtotals = sales_data[sales_data['subtotal'] > 0]
negative_subtotals = sales_data[sales_data['subtotal'] < 0]

# Merge the positive and negative subtotals to find matching invoice pairs (same item, positive = abs(negative))
merged_subtotals = pd.merge(positive_subtotals, negative_subtotals, 
                             on=['item_name'], 
                             suffixes=('_pos', '_neg'))

# Filter for cases where the positive subtotal is equal to the absolute value of the negative subtotal
merged_subtotals = merged_subtotals[merged_subtotals['subtotal_pos'] == -merged_subtotals['subtotal_neg']]

# Get the top 50 unique invoice pairs with the largest positive subtotals
top_50_pairs = merged_subtotals.drop_duplicates(subset=['subtotal_pos']).nlargest(50, 'subtotal_pos')

# Create a column for invoice pairs (invoice1/invoice2)
top_50_pairs['invoice_pair'] = top_50_pairs.apply(lambda row: f"{row['invoice_pos']}/{row['invoice_neg']}", axis=1)

# Prepare the data for the bar chart (with invoice pairs and subtotal values)
top_50_pairs['total_subtotal'] = top_50_pairs['subtotal_pos']

# Create the first bar chart (negative amounts) using Plotly
negative_amounts = sales_data[(sales_data['subtotal'] < 0) | (sales_data['net_amount'] < 0)]
negative_invoice_counts = negative_amounts[['invoice']].value_counts().reset_index()
negative_invoice_counts.columns = ['invoice', 'negative_count']
negative_invoice_counts['invoice'] = negative_invoice_counts['invoice'].astype(str)

# Create the first bar chart using Plotly (Invoices with Negative Amounts)
import plotly.express as px

fig_negative = px.bar(
    negative_invoice_counts,
    x='invoice',
    y='negative_count',
    title="Invoices with Negative Amounts",
    labels={'negative_count': 'Negative Amount Count', 'invoice': 'Invoice Number'},
    color='negative_count',
    color_continuous_scale='Viridis',
    height=600
)

# Update the layout to show invoice numbers on the x-axis only
fig_negative.update_layout(
    xaxis=dict(title_text="Invoice Number", title_font_size=14, tickangle=45),
    yaxis=dict(title_text="Negative Amount Count", title_font_size=14)
)

# Show the plot
fig_negative.show()

# Plot the second bar chart for the top 50 invoice pairs with their total subtotal values using Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(top_50_pairs['invoice_pair'], top_50_pairs['total_subtotal'], color='lightblue')

# Set the title and labels
plt.title("Top 50 Invoice Pairs with equal negative and positive Subtotal Values")
plt.xlabel("Invoice Pair (Invoice1/Invoice2)")
plt.ylabel("Subtotal Value")
plt.xticks(rotation=45, ha='center')
plt.tight_layout()

# Show the second bar chart
plt.show()

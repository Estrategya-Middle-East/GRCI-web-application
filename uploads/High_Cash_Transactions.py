import pandas as pd
import matplotlib.pyplot as plt

# Load the pickle file
pickle_path = "sales_data.pkl"
sales_data = pd.read_pickle(pickle_path)

# Rename columns for consistency
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

# Risk 5: High-Cash Transactions (Large net amounts with cash invoices)
high_cash_transactions = sales_data[(sales_data['cash_invoice'] == 'Cash') & (sales_data['net_amount'] > 1000)]

# Sort by net amount in descending order and get the top 50 high cash transactions
high_cash_transactions_sorted = high_cash_transactions.sort_values(by='net_amount', ascending=False).head(50)

# Print the count of high-cash transactions
print(f"Top 50 high cash transactions: {len(high_cash_transactions_sorted)}")

# Optionally save to a CSV for further review
high_cash_transactions_sorted.to_csv("top_50_high_cash_transactions.csv", index=False)

# Display the first few rows of the high cash transactions
print(high_cash_transactions_sorted.head())

# Plotting the top 50 high-cash transactions (e.g., net amount by invoice)
plt.figure(figsize=(12, 6))

# Treat invoice as categorical by converting it to a string
high_cash_transactions_sorted['invoice'] = high_cash_transactions_sorted['invoice'].astype(str)

# Create a bar chart with invoice numbers on the x-axis
plt.bar(high_cash_transactions_sorted['invoice'], high_cash_transactions_sorted['net_amount'], color='red')

# Set title and labels
plt.title('Top 50 High Cash Transactions', fontsize=16)
plt.xlabel('Invoice Number', fontsize=12)
plt.ylabel('Net Amount', fontsize=12)

# Rotate x-axis labels to avoid overlap and ensure only invoice numbers appear
plt.xticks(rotation=45, ha='right')

# Adjust layout for better readability
plt.tight_layout()

# Show the plot
plt.show()

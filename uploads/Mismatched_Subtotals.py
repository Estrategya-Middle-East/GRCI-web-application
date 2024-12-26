import pandas as pd

# Load the pickle file
pickle_path = "sales_data.pkl"
sales_data = pd.read_pickle(pickle_path)

# Rename columns for consistency
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

# Calculate the expected subtotal
# Calculate the expected subtotal considering the sign of qty_shipped and item_price
sales_data['expected_subtotal'] = sales_data['qty_shipped'] * sales_data['item_price'] * \
    sales_data[['qty_shipped', 'item_price']].apply(lambda x: -1 if (x[0] <= 0 and x[1] <= 0) or (x[0] > 0 and x[1] < 0) else 1, axis=1)


# Identify mismatches where the absolute difference exceeds a small tolerance
tolerance = 0.01  # Set tolerance for floating-point calculations
sales_data['discrepancy'] = abs(sales_data['subtotal'] - sales_data['expected_subtotal'])

# Filter mismatched rows
mismatched_subtotals = sales_data[sales_data['discrepancy'] > tolerance]

# Count mismatches
num_mismatches = len(mismatched_subtotals)
print(f"Number of mismatched subtotals: {num_mismatches}")

# Summarize discrepancies
discrepancy_summary = mismatched_subtotals[['invoice', 'item_name', 'qty_shipped', 'item_price', 'subtotal', 'expected_subtotal', 'discrepancy']]
print(discrepancy_summary.head())

# Save mismatched rows to a CSV for review
mismatched_subtotals.to_csv("mismatched_subtotals.csv", index=False)

# Visualize the mismatched subtotals
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.hist(mismatched_subtotals['subtotal'] - mismatched_subtotals['expected_subtotal'], bins=50, color='orange', edgecolor='black')
plt.title("Distribution of Subtotal Discrepancies")
plt.xlabel("Discrepancy Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Load the sales data
pickle_path = "sales_data.pkl"
sales_data = pd.read_pickle(pickle_path)

# Rename columns for consistency (adjust the column names as needed)
sales_data.columns = [
    "branch", "branch_name", "account", "invoice", "i", "item_number", 
    "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
    "inv_date", "reference", "cash_invoice"
]

# Prepare the feature set (using 'item_price', 'qty_shipped', and 'net_amount' for anomaly detection)
features = sales_data[['item_price', 'qty_shipped', 'net_amount']]  # You can adjust the features used here

# Train an Isolation Forest model to detect anomalies
model = IsolationForest(contamination=0.01, random_state=42)  # Adjust contamination if needed (0.01 = 1% outliers)
sales_data['unusual_price'] = model.fit_predict(features)

# Convert -1 (anomalies) to True and 1 (normal) to False
sales_data['unusual_price'] = sales_data['unusual_price'] == -1

# Filter out only the unusual prices (True values)
unusual_prices = sales_data[sales_data['unusual_price']]

# Limit to the top 100 unusual prices (based on 'item_price')
top_100_unusual = unusual_prices.nlargest(100, 'item_price')

# Plot the distribution of item prices with enhanced visuals
plt.figure(figsize=(10, 6))

# Plotting the distribution of item prices
plt.hist(sales_data['item_price'], bins=50, color='lightblue', edgecolor='black', alpha=0.7, label='Item Prices')

# Highlight the top 100 unusual prices with red markers
plt.scatter(top_100_unusual['item_price'], 
            [0]*len(top_100_unusual), 
            color='red', s=50, label='Unusual Prices', zorder=5)

# Add labels and title
plt.title('Distribution of Item Prices with Unusual Prices Highlighted by Anomaly Detection (Using AI)', fontsize=14)
plt.xlabel('Item Price', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# Add a legend
plt.legend()

# Add gridlines for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Set axis limits to zoom in on the data
plt.xlim(-50, 150)  # Adjust the x-axis limits if needed
plt.ylim(0, 175000)  # Adjust the y-axis limits if needed

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()

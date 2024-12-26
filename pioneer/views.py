import requests
import re
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import ChatMessage
from django.views.generic import TemplateView, View
from .forms import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering plots
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.offline as plot
import mpld3
import io
import base64
import datetime
from sklearn.ensemble import IsolationForest


# ERM Dashboard View
def dashboard(request):
    components = [
        {"name": "Automate risk assessment", "icon": "fas fa-cogs", "link": "#"},
        {"name": "Decision risk assessment", "icon": "fas fa-balance-scale", "link": "#"},
        {"name": "Predictive risk assessment", "icon": "fas fa-chart-line", "link": "predictive-risk-analysis/"},
        {"name": "Trend Analysis", "icon": "fas fa-chart-area", "link": "#"},
        {"name": "Root cause analysis", "icon": "fas fa-search", "link": "#"},
        {"name": "Ask PioNeer", "icon": "fas fa-brain", "link": "chat"},
    ]
    context = {
        'page_title': "PioNeer+ Dashboard",
        'components': components,
    }
    return render(request, 'chat/dashboard.html', context)


def generate_response(prompt):
    try:
        # Format the conversation history
        #history = "\n".join(
        #    [f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history]
        #)
        
        # Add the user's new input
        full_prompt = prompt
        
        # Make the API request to the model
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "llama3.2:1b", "prompt": full_prompt},
            headers={"Content-Type": "application/json"},
            stream=True,
        )
        response.raise_for_status()

        # Collect the streamed response
        final_response = ""
        for chunk in response.iter_lines():
            if chunk:  # Skip empty lines
                data = chunk.decode("utf-8")
                import json
                parsed_chunk = json.loads(data)
                final_response += parsed_chunk.get("response", "")

        return final_response.strip()
    except requests.RequestException as e:
        return f"Error: {e}"

def format_response(response):
    """
    Converts **bold** text markers to <strong> for HTML rendering.
    """
    # Replace **text** with <strong>text</strong>
    formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    return formatted_response


def chat_view(request):
    if request.method == "POST":
        form = ChatInputForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']

            # Save the user's message
            ChatMessage.objects.create(role="user", content=prompt)

            # Retrieve the entire conversation history
            conversation_history = list(
                ChatMessage.objects.order_by("timestamp").values("role", "content")
            )

            # Generate the assistant's response
            response = generate_response(prompt)
            if response:
                ChatMessage.objects.create(role="assistant", content=response)
            else:
                messages.error(request, "Failed to generate a response.")
        else:
            messages.error(request, "Invalid input. Please try again.")
    else:
        form = ChatInputForm()

    # Fetch all messages to display
    chat_messages = ChatMessage.objects.all().order_by("timestamp")

    context = {
        "page_title": "Ask PioNeer",
        "form": form,
        "chat_messages": chat_messages,
    }

    return render(request, "chat/chat.html", context)

def clear_chat(request):
    if request.method == "POST":
        ChatMessage.objects.all().delete()
        return JsonResponse({"status": "success", "message": "Chat cleared."})
    return redirect("chat")



def ajax_chat(request):
    if request.method == "POST":
        form = ChatInputForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]

            # Save the user message
            user_message = ChatMessage(role="user", content=prompt)
            user_message.save()

            # Retrieve the conversation history
            conversation_history = ChatMessage.objects.order_by("timestamp").values("role", "content")

            # Generate AI response
            try:
                response = generate_response(prompt)

                # Save assistant response
                assistant_message = ChatMessage(role="assistant", content=response)
                assistant_message.save()

                return JsonResponse({"status": "success", "response": response})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Failed to process your message. {str(e)}"}, status=500)
        else:
            return JsonResponse({"status": "error", "message": "Invalid form submission."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


def sheet(request):

    # Define the path to the Excel file
    excel_file = r'C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\hwb_2015.xlsx'

    # Read each sheet and store it in the dictionary

    df = pd.read_excel(excel_file, sheet_name='Sales Data')

    # Display the first 5 rows of each sheet
    #print(df.head(), "\n")
    data = df.head().to_dict(orient='records')
    return render(request, 'erm/sheet_table.html', {'data': data})


class PredictiveRiskAnalysisView(View):
    def get(self, request, *args, **kwargs):
        # Instantiate the form on GET request
        form = RiskAnalysisForm()
        return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', 
                {'form': form,
                "page_title": "Predictive Risk",
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,})

    def post(self, request, *args, **kwargs):
        form = RiskAnalysisForm(request.POST)

        if form.is_valid():
            # Get the selected options
            main_category = form.cleaned_data['main_category']
            subcategory = form.cleaned_data.get('subcategory_sales_ledger')

            
            chart = None
            name= None
            chart2 = None
            name2= None
            chart3 = None
            name3= None
            chart4 = None
            name3= None
            response = None
            

            # Handle based on the selection
            if main_category == 'sales_ledger' and subcategory == 'duplicate_invoices':
               chart, chart2, chart3, name, name2, name3, response = self.generate_duplicate_invoices_graph()
            elif main_category == 'sales_ledger' and subcategory == 'negative_amount':
                chart, chart2, name, name2, response = self.generate_net_amount_graphs()
            elif main_category == 'sales_ledger' and subcategory == 'invalid_invoices':
                chart, name, response = self.generate_invalid_invoices_garphs()
            elif main_category == 'sales_ledger' and subcategory == 'mismatched_subtotals':
                chart, name, response = self.generate_mismatched_subtotals_garphs()
            elif main_category == 'sales_ledger' and subcategory == 'high_cash_transactions':
                chart, name, response = self.generate_high_cash_transactions_garphs()
            elif main_category == 'sales_ledger' and subcategory == 'unusual_prices':
                chart, name, response = self.generate_unusual_prices_garphs()

            # Pass the graphs to the template
            return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', {
                'form': form,
                "page_title": "Predictive Risk",
                'chart': chart,
                'chart2': chart2,
                'chart3': chart3,
                'name': name,
                'name2': name2,
                'name3': name3,
                'response': response,
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
            })
        else:
            return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', 
                {'form': form,
                "page_title": "Predictive Risk",
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,})

    def generate_duplicate_invoices_graph(self):
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
        # Load the pickle file
        try:
            sales_data = pd.read_pickle(pickle_path)
        except Exception as e:
            raise ValueError(f"Error loading data from {pickle_path}: {str(e)}")

        # Rename columns for easier access
        sales_data.columns = [
            "branch", "branch_name", "account", "invoice", "i", "item_number", 
            "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
            "inv_date", "reference", "cash_invoice"
        ]
        
        

        

        # Count duplicates for each invoice
        invoice_counts = sales_data['invoice'].value_counts()

        # Filter only duplicates (more than 1 occurrence)
        duplicate_invoice_counts = invoice_counts[invoice_counts > 1]

        # Convert to DataFrame for plotting
        duplicate_invoice_summary = duplicate_invoice_counts.reset_index()
        duplicate_invoice_summary.columns = ['invoice', 'count']

        # Display summary
        #print(duplicate_invoice_summary.head())
        data= duplicate_invoice_summary.head().to_dict(orient="records")

        
        # Limit to top 20 duplicate invoices for visualization
        top_duplicates = duplicate_invoice_summary.head(20)
        top_20 = duplicate_invoice_summary.head(20).to_dict(orient="records")

        # Create a bar plot
        fig = plt.figure(figsize=(5, 4))
        sns.barplot(data=top_duplicates, x='invoice', y='count', palette="viridis")

        # Add labels and title
        
        plt.xlabel("Invoice Number", fontsize=12)
        plt.ylabel("Duplicate Count", fontsize=12)
        plt.xticks(rotation=45, ha='center')
        plt.tight_layout()
        #plt.show()
        chart3 = mpld3.fig_to_html(fig)
        name3= "Top 20 Duplicate Invoices"

        # Sort and select top 100 duplicate invoices
        top_100_duplicates = duplicate_invoice_summary.sort_values(by='count', ascending=False).head(100)

        # Convert 'invoice' to a string to ensure it's treated as a category
        top_100_duplicates['invoice'] = top_100_duplicates['invoice'].astype(str)

        # Create the bar plot
        fig_bar = px.bar(
        top_100_duplicates,
        x='invoice', 
        y='count',
        labels={'count': 'Duplicate Count', 'invoice': 'Invoice Number'},
        color='count',
        color_continuous_scale='Viridis',
        height=400,
        width=500,
        )

        # Update x-axis settings
        bar_data= fig_bar.update_layout(
        xaxis=dict(title_text="Invoice Number", title_font_size=14, categoryorder="total descending", tickangle=45),
        yaxis=dict(title_text="Duplicate Count", title_font_size=14)
        )

        # Show the plot
        #fig_bar.show()
        chart = plot.plot(bar_data, output_type="div")
        name ="Top 100 Duplicate Invoices"


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
        color='Type',
        color_discrete_map={"Unique Invoices": "blue", "Duplicate Invoices": "orange"}
        )

        # Show the pie chart
        #fig_pie.show()
        chart2 = plot.plot(fig_pie, output_type="div")
        name2="Distribution of Duplicate vs Unique Invoices"
        
        # Prepare text for LLM prompt
        if not duplicate_invoice_summary.empty:
            duplicate_invoice_text = duplicate_invoice_summary.sort_values(by='count', ascending=False).to_string(index=False)
            llm_prompt = f"The following duplicate invoices were found in the dataset:\n{duplicate_invoice_text}\n\nAs a business/data analyst, please analyze the implications of these duplicate invoices on the business operations. Consider potential causes of these duplicates (e.g., system errors, data entry mistakes, etc.), and suggest practical solutions for preventing them. Additionally, discuss the potential impact on financial reporting, customer trust, and operational efficiency."
        else:
            llm_prompt = "No duplicate invoices were found in the dataset. As a business/data analyst, please analyze the implications of having only unique invoices. Consider the positive effects on data integrity, operational efficiency, and the accuracy of financial reporting. Also, discuss how maintaining unique invoices contributes to trust and transparency with customers and stakeholders."
        
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart, chart2, chart3, name, name2, name3, response
    
    def generate_net_amount_graphs(self):
        # Load the pickle file
        # Load the pickle file
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
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


        fig_negative = px.bar(
            negative_invoice_counts,
            x='invoice',
            y='negative_count',
            labels={'negative_count': '-ve Amount Count', 'invoice': 'Invoice Number'},
            color='negative_count',
            color_continuous_scale='Viridis',
            height=400,
            width= 500
        )

        # Update the layout to show invoice numbers on the x-axis only
        bar_data = fig_negative.update_layout(
            xaxis=dict(title_text="Invoice Number", title_font_size=14, tickangle=45),
            yaxis=dict(title_text="-ve Amount Count", title_font_size=14)
        )

        # Show the plot
        #fig_negative.show()
        chart = plot.plot(bar_data, output_type="div")
        name ="Invoices with Negative Amounts"

        # Plot the second bar chart for the top 50 invoice pairs with their total subtotal values using Matplotlib
        fig = plt.figure(figsize=(5, 4))
        plt.bar(top_50_pairs['invoice_pair'], top_50_pairs['total_subtotal'], color='lightblue')

        # Set the title and labels
        plt.xlabel("Invoice Pair (Invoice1/Invoice2)")
        plt.ylabel("Subtotal Value")
        plt.xticks(rotation=45, ha='center')
        plt.tight_layout()

        # Convert the Matplotlib plot to an interactive HTML div
        chart2 = mpld3.fig_to_html(fig)
        name2= "Top 50 Invoice Pairs with Equal -ve and +ve Subtotal Values"
        
        if len(top_50_pairs) > 0:
            llm_prompt = (
                f"The dataset contains {len(negative_invoice_counts)} invoices with negative amounts, "
                f"and {len(top_50_pairs)} top matching invoice pairs where positive subtotals "
                f"equal the absolute value of negative subtotals. "
                "Analyze the potential reasons for these patterns and recommend measures to prevent negative entries where applicable."
            )
        else:
            llm_prompt = (
                "The dataset contains no matching invoice pairs with equal negative and positive subtotal values. "
                "This suggests a clean dataset in terms of balancing positive and negative subtotals. "
                "Confirm if further checks are needed or recommend additional areas of analysis."
            )
        
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        
        return chart, chart2, name, name2, response

    def generate_invalid_invoices_garphs(self):
        # Load the pickle file
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
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
        #print(f"Number of invalid invoice dates: {len(invalid_dates)}")
        #print(invalid_dates[['invoice', 'inv_date']].head())

        # Save invalid dates to a CSV for further review (optional)
        #invalid_dates.to_csv("invalid_invoice_dates.csv", index=False)

        # Visualize invalid dates
        num_invalid_invoices = len(invalid_dates)
    
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
            labels={'inv_date': 'Invoice Date', 'count': 'Number of Invalid Entries'},
            markers=True,
            height= 400,
            width= 550
        )

        # Show the plot
        #fig_invalid_dates.show()
        chart = plot.plot(fig_invalid_dates, output_type="div")
        name="Invalid Invoice Dates Over Time"
        
        if num_invalid_invoices > 0:
            llm_prompt = (
                f"There are {num_invalid_invoices} invoices with invalid dates in the dataset. "
                f"The valid date range is from {valid_start_date.strftime('%Y-%m-%d')} to {valid_end_date.strftime('%Y-%m-%d')}. "
                "These invalid dates might indicate potential issues with data entry or system errors. "
                "Please provide insights and suggest measures to mitigate such risks in the future."
            )
        
            
        else:
            llm_prompt = (
                f"All invoice dates in the dataset fall within the valid range from {valid_start_date.strftime('%Y-%m-%d')} "
                f"to {valid_end_date.strftime('%Y-%m-%d')}. No issues were found with invoice dates. "
                "Confirm whether any additional checks are required or suggest improvements."
            )
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart,name, response #, chart2
       
    def generate_mismatched_subtotals_garphs(self):
        # Load the pickle file
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
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
        #print(f"Number of mismatched subtotals: {num_mismatches}")

        # Summarize discrepancies
        discrepancy_summary = mismatched_subtotals[['invoice', 'item_name', 'qty_shipped', 'item_price', 'subtotal', 'expected_subtotal', 'discrepancy']]
        #print(discrepancy_summary.head())

        # Save mismatched rows to a CSV for review
        #mismatched_subtotals.to_csv("mismatched_subtotals.csv", index=False)

        # Visualize the mismatched subtotals
        fig = plt.figure(figsize=(5, 4))
        plt.hist(mismatched_subtotals['subtotal'] - mismatched_subtotals['expected_subtotal'], bins=50, color='orange', edgecolor='black')
        
        plt.xlabel("Discrepancy Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        #plt.show()
        
        chart = mpld3.fig_to_html(fig)
        name= "Distribution of Subtotal Discrepancies"
        
        if num_mismatches > 0:
            llm_prompt = (
                f"There are {num_mismatches} items with mismatched subtotals in the dataset. "
                f"These discrepancies are calculated based on a tolerance of {tolerance}. "
                "The mismatches might indicate potential data entry errors or inconsistencies in pricing or quantities. "
                "Please provide insights on the possible reasons for these discrepancies and suggest measures to prevent such issues in the future."
            )
        else:
            llm_prompt = (
                f"All subtotals in the dataset match the expected calculations within a tolerance of {tolerance}. "
                "No issues were detected. Confirm whether any additional checks are required or provide recommendations for further analysis."
            )
        
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart,name, response #, chart2
    
    def generate_high_cash_transactions_garphs(self):
        # Load the pickle file
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
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
        #print(f"Top 50 high cash transactions: {len(high_cash_transactions_sorted)}")

        # Optionally save to a CSV for further review
        #high_cash_transactions_sorted.to_csv("top_50_high_cash_transactions.csv", index=False)

        # Display the first few rows of the high cash transactions
        #print(high_cash_transactions_sorted.head())
        
        
        # Prepare a summary of the high-cash transactions for the LLM
        transaction_summary = high_cash_transactions_sorted[['invoice', 'branch_name', 'net_amount']]
        # Convert the summary to a string for the LLM prompt
        summary_str = transaction_summary.to_string(index=False)

        # Generate an LLM prompt
        llm_prompt = f"""
        The following is a summary of the top 50 high-cash transactions at various branches:

        {summary_str}

        From a business perspective, please analyze the potential risks associated with these high-cash transactions. 
        Consider possible factors like operational inefficiencies, risks of fraud, and the impact on financial controls. 
        Additionally, provide strategic recommendations to address these risks, such as strengthening internal controls, 
        enhancing transaction monitoring, or implementing better compliance measures.
        """
        #conversation_history = 1
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        # Plotting the top 50 high-cash transactions (e.g., net amount by invoice)
        fig = plt.figure(figsize=(5, 4))

        # Treat invoice as categorical by converting it to a string
        high_cash_transactions_sorted['invoice'] = high_cash_transactions_sorted['invoice'].astype(str)

        # Create a bar chart with invoice numbers on the x-axis
        plt.bar(high_cash_transactions_sorted['invoice'], high_cash_transactions_sorted['net_amount'], color='red')

        # Set title and labels
        
        plt.xlabel('Invoice Number', fontsize=12)
        plt.ylabel('Net Amount', fontsize=12)

        # Rotate x-axis labels to avoid overlap and ensure only invoice numbers appear
        plt.xticks(rotation=45, ha='right')

        # Adjust layout for better readability
        plt.tight_layout()
        
        # Show the plot
        #plt.show()
        chart = mpld3.fig_to_html(fig)
        name = 'Top 50 High Cash Transactions'
        
        return chart, name, response #, chart2
    
    def generate_unusual_prices_garphs(self):
        # Load the sales data
        pickle_path = r"C:\Users\Mostafa\IAM-App\GRCI-web-application\uploads\sales_data.pkl"
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
        fig = plt.figure(figsize=(5, 4))

        # Plotting the distribution of item prices
        plt.hist(sales_data['item_price'], bins=50, color='lightblue', edgecolor='black', alpha=0.7, label='Item Prices')

        # Highlight the top 100 unusual prices with red markers
        plt.scatter(top_100_unusual['item_price'], 
                    [0]*len(top_100_unusual), 
                    color='red', s=50, label='Unusual Prices', zorder=5)

        # Add labels and title
        
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
        #plt.show()
        
        chart = mpld3.fig_to_html(fig)
        name='Distribution of Item Prices with Unusual Prices Highlighted by Anomaly Detection (Using AI)'
        
        # Prepare the LLM prompt
        if len(top_100_unusual) > 0:
            # Create a high-level abstract prompt for the LLM
            llm_prompt = (
                "Unusual pricing patterns have been detected in the sales data. "
                "Please analyze the potential business implications of these anomalies. "
                "Consider the broader impact on business operations, financial forecasting, "
                "customer trust, and internal processes. Discuss possible systemic causes of these anomalies "
                "and recommend strategic actions to address any risks associated with pricing irregularities, "
                "including their impact on organizational reputation and long-term performance."
            )
        else:
            # If no unusual prices were found
            llm_prompt = (
                "The sales data shows consistent pricing without any noticeable anomalies. "
                "Please analyze the positive implications of having a dataset with stable and reliable pricing. "
                "Discuss how this consistency can support business operations, improve financial accuracy, "
                "and enhance trust with customers and stakeholders. Consider the long-term benefits of maintaining "
                "a stable pricing model and its effect on overall operational efficiency and business growth."
            )
        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart,name, response #, chart2
        

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
from datetime import datetime, timedelta
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
            json={"model": "llama3.2:1b", "prompt": full_prompt}, # llama3.1:8b
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
            response = format_response(response)
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
    excel_file = r'./uploads/hwb_2015.xlsx'

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
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
                'purchase_order_choices': RiskAnalysisForm.suboptions_purchase_order,})

    def post(self, request, *args, **kwargs):
        form = RiskAnalysisForm(request.POST)

        if form.is_valid():
            # Get the selected options
            main_category = form.cleaned_data['main_category']
            subcategory_sales_ledger = form.cleaned_data.get('subcategory_sales_ledger')
            subcategory_purchase_order = form.cleaned_data.get('subcategory_purchase_order')

            
            chart = None
            name= None
            chart2 = None
            name2= None
            chart3 = None
            name3= None
            chart4 = None
            name4= None
            response = None
            

            # Handle based on the selection
            if main_category == 'sales_ledger': 
                if subcategory_sales_ledger == 'duplicate_invoices':
                    chart, chart2, chart3, name, name2, name3, response = self.generate_duplicate_invoices_graph()
                elif subcategory_sales_ledger == 'negative_amount':
                    chart, chart2, name, name2, response = self.generate_net_amount_graphs()
                elif subcategory_sales_ledger == 'invalid_invoices':
                    chart, name, response = self.generate_invalid_invoices_garphs()
                elif subcategory_sales_ledger == 'mismatched_subtotals':
                    chart, name, response = self.generate_mismatched_subtotals_garphs()
                elif subcategory_sales_ledger == 'high_cash_transactions':
                    chart, name, response = self.generate_vendor_performance_risk()
                elif subcategory_sales_ledger == 'unusual_prices':
                    chart, name, response = self.generate_vendor_status()
            
            if main_category == 'purchase_order': 
                if subcategory_purchase_order == 'delayed_po_approvals':
                    chart, chart3, name, name3, response = self.generate_delayed_po_approvals_graphs()
                elif subcategory_purchase_order == 'open_pos':
                    chart, name, response = self.generate_open_pos()
                elif subcategory_purchase_order == 'quantity_mistmatch':
                    chart, name, response = self.generate_quantity_mistmatch()
                elif subcategory_purchase_order == 'vendor_performance_risk':
                    chart4, name4, response = self.generate_vendor_performance_risk()
                elif subcategory_purchase_order == 'vendor_status':
                    chart, chart2, name,  name2, response = self.generate_vendor_status()

            # Pass the graphs to the template
            return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', {
                'form': form,
                "page_title": "Predictive Risk",
                'chart': chart,
                'chart2': chart2,
                'chart3': chart3,
                'chart4': chart4,
                'name': name,
                'name2': name2,
                'name3': name3,
                'name4': name4,
                'response': response,
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
                'purchase_order_choices': RiskAnalysisForm.suboptions_purchase_order,
            })
        else:
            return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', 
                {'form': form,
                "page_title": "Predictive Risk",
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
                'purchase_order_choices': RiskAnalysisForm.suboptions_purchase_order,})

    def generate_duplicate_invoices_graph(self):
        pickle_path = r"./uploads/sales_data.pkl"
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
        pickle_path = r"./uploads/sales_data.pkl"
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
        pickle_path = r"./uploads/sales_data.pkl"
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
        pickle_path = r"./uploads/sales_data.pkl"
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
        pickle_path = r"./uploads/sales_data.pkl"
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
        pickle_path = r"./uploads/sales_data.pkl"
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

    # purchase orders
    def generate_delayed_po_approvals_graphs(self):
        file_path = r"./uploads/PO_EXTRACT.xls"  # Replace with the path to your .xls file
        data = pd.read_excel(file_path)

        # Step 2: Ensure date columns are in datetime format
        data['PO_CREATION_DATE'] = pd.to_datetime(data['PO_CREATION_DATE'], errors='coerce')
        data['APPROVED_DATE'] = pd.to_datetime(data['APPROVED_DATE'], errors='coerce')

        # Step 3: Calculate the delay in days
        data['Approval_Delay_Days'] = (data['APPROVED_DATE'] - data['PO_CREATION_DATE']).dt.days

        # Step 4: Flag delayed approvals (e.g., delays greater than 7 days)
        delay_threshold = 7  # Define the delay threshold in days
        data['Delayed_Approval'] = data['Approval_Delay_Days'] > delay_threshold

        # Step 5: Extract data for LLM prompt
        # Top delayed POs
        delayed_pos = data[data['Delayed_Approval']].sort_values(by='Approval_Delay_Days', ascending=False).head(3)
        top_delayed_pos = delayed_pos[['PO_NUMBER', 'Approval_Delay_Days']].to_dict('records')

        # Approval delay range
        approval_delay_min = data['Approval_Delay_Days'].min()
        approval_delay_max = data['Approval_Delay_Days'].max()


        ## Option 1: Bar Chart of Delayed vs. On-Time Approvals
        delay_counts = data['Delayed_Approval'].value_counts()

        fig1 = plt.figure(figsize=(5, 4))
        sns.barplot(x=delay_counts.index, y=delay_counts.values, palette="viridis")
        plt.xticks([0, 1], ["On Time", "Delayed"])
        plt.xlabel("Approval Status")
        plt.ylabel("Number of POs")
        
        
        chart = mpld3.fig_to_html(fig1)
        name = "Delayed vs. On-Time PO Approvals"
        
        # Step 6: Visualization (Optional)
        fig2 = plt.figure(figsize=(5, 4))
        sns.histplot(data['Approval_Delay_Days'].dropna(), bins=30, kde=True, color='blue')
        plt.axvline(delay_threshold, color='red', linestyle='--', label="Threshold (7 Days)")
        plt.xlabel("Approval Delay (Days)")
        plt.ylabel("Number of POs")
        plt.legend()
        
        
        name3 = "Distribution of PO Approval Delays"
        chart3 = mpld3.fig_to_html(fig2)
        
        # Step 7: LLM Prompt
        llm_prompt = f"""
        You are a Governance, Risk, and Compliance (GRC) expert. Analyze the following Purchase Order (PO) data for potential risks and suggest improvements.

        Data Summary:
        - Each purchase order (PO) contains the following attributes: PO_NUMBER, PO_CREATION_DATE, APPROVED_DATE, PO_STATUS, QUANTITY, QUANTITY_RECEIVED, QUANTITY_CANCELLED, AMOUNT, CLOSURE_STATUS, and SUPPLIER_COUNTRY.
        - A delay in approval is flagged when the time between PO_CREATION_DATE and APPROVED_DATE exceeds {delay_threshold} days.

        Identified Risk 1: Delayed PO Approvals
        - Some POs have approval delays exceeding {delay_threshold} days, which may impact timely procurement and project delivery.
        - Examples of delayed POs:
        {top_delayed_pos}
        - Approval delay (days): {approval_delay_min}-{approval_delay_max}.

        Instructions:
        1. Analyze the risk of delayed PO approvals and its potential impact on procurement processes and operations.
        2. Suggest specific process improvements or controls to mitigate the delays and improve efficiency in the PO approval process.
        3. Highlight any additional risks you identify in the provided PO data, such as:
        - Quantity mismatches (e.g., received quantities not matching ordered quantities).
        - Excessive cancellations.
        - Financial discrepancies (e.g., mismatched amounts or currencies).
        - Supplier-related risks (e.g., inactive suppliers, high-risk countries, or inconsistent statuses).
        4. Propose a risk management framework for addressing the identified issues and ensuring compliance with procurement policies.

        Key Context:
        - The organization operates internationally, and the data contains POs from various countries.
        - The goal is to minimize operational, financial, and compliance risks in the procurement process.
        """

        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart, chart3, name, name3, response

    def generate_open_pos(self):
        # Step 1: Load the Excel file
        file_path = r"./uploads/PO_EXTRACT.xls"  # The provided file name
        data = pd.read_excel(file_path)

        # Step 2: Filter for Open POs
        open_pos = data[data['CLOSURE_STATUS'] == 'OPEN']

        # Step 3: Define threshold for 'not updated' POs
        # For this example, consider POs not updated for more than 30 days as problematic
        threshold_date = datetime.now() - timedelta(days=30)

        # Step 4: Identify POs that have not been updated within the threshold period
        open_pos['PO_LAST_UPDATE_DATE'] = pd.to_datetime(open_pos['PO_LAST_UPDATE_DATE'], errors='coerce')
        not_updated_pos = open_pos[open_pos['PO_LAST_UPDATE_DATE'].isna() | (open_pos['PO_LAST_UPDATE_DATE'] < threshold_date)]

        # Sort POs by the number of days since last update (older to newer)
        not_updated_pos['Days_Since_Update'] = (datetime.now() - not_updated_pos['PO_LAST_UPDATE_DATE']).dt.days
        not_updated_pos_sorted = not_updated_pos.sort_values(by='Days_Since_Update', ascending=False)

        # Limit to the first 50 entries or fewer
        not_updated_pos_top50 = not_updated_pos_sorted['PO_NUMBER'].value_counts().head(50)

        # Step 5: Visualizing the Risk - Graph for Open POs Not Updated
        fig = plt.figure(figsize=(5, 4))
        bars = plt.bar(not_updated_pos_top50.index.astype(str), not_updated_pos_top50.values, color='red')
        plt.xlabel("PO Number")
        plt.ylabel("Count of Open POs Not Updated")

        # Rotate the x-axis labels to make them readable and adjust layout
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Open POs Not Updated (Older than 30 Days)"

        # Step 6: Prepare LLM Prompt for Analysis
        llm_prompt = f"""
        You are a Governance, Risk, and Compliance (GRC) expert. Analyze the following Purchase Order (PO) data for potential risks and suggest improvements.

        Data Summary:
        - We are analyzing **Open POs** that have not been updated in over 30 days, which could indicate potential delays or unresolved issues.
        - A Purchase Order (PO) is considered problematic if the **PO_LAST_UPDATE_DATE** is missing or outdated (older than 30 days).

        Identified Risk 5: Open POs Not Updated
        - Open POs that have not been updated in a timely manner can lead to procurement delays, inventory mismanagement, and overall inefficiencies in the supply chain.
        - The data shows the number of **open POs** that have not been updated in the past 30 days.

        Examples of at-risk POs (first 50):
        {not_updated_pos_top50.to_dict()}

        Opportunities for Improvement:
        - If many POs have not been updated recently, it suggests a need for better monitoring or automated alerts to ensure timely updates.
        - Consider implementing automated systems to track PO status and updates more efficiently or assign dedicated personnel to review and update open POs regularly.

        Instructions:
        1. Analyze the risk of open POs that have not been updated recently, considering potential disruptions to the procurement process.
        2. Suggest improvements, such as regular reviews of open POs, automated status tracking, or stronger follow-up mechanisms to ensure that open POs are updated promptly.
        """

        # Print the prompt for input to the LLM
        response = generate_response(llm_prompt)
        response = format_response(response)

        return chart, name, response

    def generate_quantity_mistmatch(self):
        # Step 1: Load the Excel file
        file_path = r"./uploads/PO_EXTRACT.xls"  # The provided file name
        data = pd.read_excel(file_path)

        # Step 2: Analyze Quantity Mismatches
        # Calculate mismatch metrics
        data['Quantity_Mismatch'] = data['QUANTITY'] - data['QUANTITY_RECEIVED'] - data['QUANTITY_CANCELLED']

        # Identify significant mismatches (e.g., mismatch > 10 units or mismatch > 20% of ordered quantity)
        data['Significant_Mismatch'] = (data['Quantity_Mismatch'] > 10) | (data['Quantity_Mismatch'] > 0.2 * data['QUANTITY'])

        # Filter the data to include only significant mismatches
        significant_data = data[data['Significant_Mismatch']]

        # Step 3: Sort and Select the Top 50 Mismatches (or fewer if less than 50 available)
        top_mismatches = significant_data.sort_values(by='Quantity_Mismatch', ascending=False).head(50)

        # Extract top mismatched POs for LLM prompt
        top_mismatched_pos = top_mismatches[['PO_NUMBER', 'QUANTITY', 'QUANTITY_RECEIVED', 'QUANTITY_CANCELLED', 'Quantity_Mismatch']].to_dict('records')

        # Calculate mismatch statistics
        total_mismatches = top_mismatches['Significant_Mismatch'].sum()
        average_mismatch = top_mismatches['Quantity_Mismatch'].mean()

        # Step 4: Visualization
        fig = plt.figure(figsize=(5, 4))

        # Create a bar plot using only PO numbers with significant mismatches
        bars = plt.bar(top_mismatches['PO_NUMBER'].astype(str), top_mismatches['Quantity_Mismatch'], color='red', label='Quantity Mismatch')

        # Add annotations for significant mismatches
        for i, row in top_mismatches.iterrows():
            plt.text(i, row['Quantity_Mismatch'] + 2, f"{row['Quantity_Mismatch']:.1f}", ha='center', fontsize=9, color='black')

        # Enhance titles and labels
        #plt.title("Top Significant Quantity Mismatches Across Purchase Orders", fontsize=16, fontweight='bold')
        plt.xlabel("Purchase Order Numbers (PO_NUMBER)", fontsize=12)
        plt.ylabel("Quantity Mismatch (Units)", fontsize=12)
        plt.xticks(rotation=45, fontsize=9)  # Rotate PO numbers for readability
        plt.yticks(fontsize=10)

        # Add legend and grid
        plt.legend(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Display the chart
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Top Significant Quantity Mismatches Across Purchase Orders"

        # Step 5: LLM Prompt
        llm_prompt = f"""
        You are a Governance, Risk, and Compliance (GRC) expert. Analyze the following Purchase Order (PO) data for potential risks and suggest improvements.

        Data Summary:
        - Each purchase order (PO) contains the following attributes: PO_NUMBER, QUANTITY, QUANTITY_RECEIVED, QUANTITY_CANCELLED, and Quantity_Mismatch.
        - A significant mismatch is flagged if the mismatch exceeds 10 units or 20% of the ordered quantity.

        Identified Risk 2: Quantity Mismatches
        - Some POs have significant mismatches between the quantities ordered, received, and canceled. This may indicate issues in supplier performance, procurement planning, or inventory management.
        - Examples of mismatched POs:
        {top_mismatched_pos}
        - Total significant mismatches: {total_mismatches}
        - Average mismatch across all POs: {average_mismatch:.2f} units.

        Instructions:
        1. Analyze the risk of quantity mismatches and its potential impact on operations, such as delayed deliveries or excess inventory.
        2. Suggest process improvements to ensure accurate quantities in procurement orders and better alignment with supplier deliveries.
        3. Highlight any additional risks you identify in the provided PO data, such as:
        - Excessive cancellations.
        - Poor supplier performance (e.g., consistent under-delivery).
        - Patterns of mismatches linked to specific suppliers or countries.

        Key Context:
        - The organization operates internationally, and the data contains POs from various countries.
        - The goal is to minimize operational, financial, and compliance risks in the procurement process.
        """

        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart, name, response


    def generate_vendor_performance_risk(self):
        # Step 1: Load the Excel file
        file_path = r"./uploads/PO_EXTRACT.xls"  # The provided file name
        data = pd.read_excel(file_path)

        # Step 2: Calculate Quantity Mismatch (difference between ordered and received quantities)
        data['Quantity_Mismatch'] = data['QUANTITY'] - data['QUANTITY_RECEIVED']

        # 2.1: Identify vendors with frequent order cancellations
        data['Cancellation_Rate'] = data['QUANTITY_CANCELLED'] / data['QUANTITY']

        # 2.2: Filter vendors with high cancellation rates (threshold > 20%)
        high_cancellation_vendors = data[data['Cancellation_Rate'] > 0.2]

        # 2.3: Vendors with many OPEN POs (PO_STATUS = "OPEN")
        open_pos_vendors = data[data['PO_STATUS'] == "OPEN"]

        # 2.4: Mismatch analysis for vendors with significant mismatches
        # Calculate Quantity Mismatch for each vendor
        vendor_mismatch = data.groupby('VENDOR_NAME')['Quantity_Mismatch'].sum()
        top_vendors_by_mismatch = vendor_mismatch.sort_values(ascending=False).head(10)

        # Step 3: Create Vendor Risk Visualization
        fig = plt.figure(figsize=(12, 8))

        plt.subplot(1, 2, 1)
        high_cancellation_vendors_grouped = high_cancellation_vendors.groupby('VENDOR_NAME').agg({'Cancellation_Rate': 'mean'}).sort_values(by='Cancellation_Rate', ascending=False)
        bars1 = plt.bar(high_cancellation_vendors_grouped.index, high_cancellation_vendors_grouped['Cancellation_Rate'], color='orange')
        plt.title("Vendors with High Cancellation Rates (>20%)")
        plt.ylabel("Cancellation Rate")
        plt.xticks(rotation=45, ha='right', fontsize=9)  # Fixing overlap with rotation and alignment
        plt.tight_layout()

        # Bar chart for top 10 vendors by quantity mismatch
        plt.subplot(1, 2, 2)
        bars2 = plt.bar(top_vendors_by_mismatch.index, top_vendors_by_mismatch.values, color='red')
        plt.title("Top 10 Vendors by Quantity Mismatch")
        plt.ylabel("Total Quantity Mismatch (Units)")
        plt.xticks(rotation=45, ha='right', fontsize=9)  # Fixing overlap with rotation and alignment
        plt.tight_layout()
        
        # Bar chart for vendors with high cancellation rates
        chart4 = mpld3.fig_to_html(fig)
        name4 = "Vendors with High Cancellation Rates"

        # Step 4: Prepare LLM Prompt
        llm_prompt = f"""
        You are a Governance, Risk, and Compliance (GRC) expert. Analyze the following Vendor Performance data for potential risks and suggest improvements.

        Data Summary:
        - We are analyzing vendor performance based on cancellation rates, POs marked as "OPEN" for extended periods, and quantity mismatches.
        - Vendors with significant risks:
        - High cancellation rates (over 20% of orders canceled).
        - Vendors with many open POs (PO_STATUS = 'OPEN').
        - Vendors with a high total quantity mismatch (difference between ordered and received quantities).

        Identified Risk 3: Vendor Performance
        - Some vendors have high cancellation rates, indicating potential issues in inventory management, forecasting, or supplier reliability.
        - Other vendors have significant quantity mismatches, which could lead to delays or procurement inefficiencies.
        - Examples of at-risk vendors:
        1. High Cancellation Rate Vendors:
        {high_cancellation_vendors[['VENDOR_NAME', 'Cancellation_Rate']].to_dict('records')}
        2. Top 10 Vendors by Quantity Mismatch:
        {top_vendors_by_mismatch.to_dict()}

        Instructions:
        1. Analyze the risk of vendor performance, considering impacts such as delayed deliveries, potential disruptions in production, and operational inefficiencies.
        2. Suggest process improvements, such as better vendor performance monitoring, improved supplier relations, or inventory forecasting tools.
        3. Identify any trends, patterns, or commonalities in vendor performance risks that could help prioritize interventions (e.g., specific suppliers or regions).
        """

        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart4, name4, response

    def generate_vendor_status(self):
        # Step 1: Load the Excel file
        file_path = r"./uploads/PO_EXTRACT.xls"  # The provided file name
        data = pd.read_excel(file_path)

        # Step 2: Identify Inactive Suppliers and Payment Discrepancies
        # Filter suppliers with status other than "ACTIVE"
        inactive_suppliers = data[data['SUPPLIER_STATUS'] != 'Active']

        # Check for missing or invalid bank account details (empty or null values)
        invalid_bank_info = data[data['BANK ACCOUNT NUMBER'].isna() | data['BANK ACCOUNT NAME'].isna()]

        # Limit to the first 50 entries or fewer
        inactive_suppliers_top50 = inactive_suppliers['VENDOR_NAME'].value_counts().head(50)
        invalid_bank_info_top50 = invalid_bank_info['VENDOR_NAME'].value_counts().head(50)

        # Step 3: Visualizing the Risk - Separate Graphs

        # Graph 1: Inactive Suppliers Chart
        fig = plt.figure(figsize=(5, 4))
        bars1 = plt.bar(inactive_suppliers_top50.index, inactive_suppliers_top50.values, color='red')
        plt.title("Inactive Suppliers")
        plt.xlabel("Vendor Name")
        plt.ylabel("Count of Inactive Suppliers")
        plt.xticks(rotation=45, ha='right', fontsize=7)
        plt.tight_layout()
        
        chart = mpld3.fig_to_html(fig)
        name = "Inactive Suppliers"

        # Graph 2: Invalid Bank Account Info Chart
        fig2 = plt.figure(figsize=(5, 6))
        bars2 = plt.bar(invalid_bank_info_top50.index, invalid_bank_info_top50.values, color='red')
        plt.title("Vendors with Invalid Bank Information")
        plt.xlabel("Vendor Name")
        plt.ylabel("Count of Invalid Bank Accounts")
        plt.xticks(rotation=45, ha='right', fontsize=7)
        plt.tight_layout()
        
        chart2 = mpld3.fig_to_html(fig2)
        name2 = "Count of Invalid Bank Accounts"
        
        # Step 4: Prepare LLM Prompt for Analysis
        inactive_suppliers_check = inactive_suppliers['SUPPLIER_STATUS'].value_counts()
        invalid_bank_check = invalid_bank_info['BANK ACCOUNT NUMBER'].isna().sum() == 0 and invalid_bank_info['BANK ACCOUNT NAME'].isna().sum() == 0

        llm_prompt = f"""
        You are a Governance, Risk, and Compliance (GRC) expert. Analyze the following Supplier Risk data for potential risks and suggest improvements.

        Data Summary:
        - We are analyzing supplier performance based on their **SUPPLIER_STATUS** (active/inactive) and the completeness of their **bank account details**.
        - Vendors with significant risks:
        - Inactive suppliers (SUPPLIER_STATUS != "ACTIVE").
        - Suppliers with missing or invalid **bank account information**.

        Identified Risk 4: Supplier Risk
        - Some suppliers are marked as inactive, which could lead to delays or interruptions in procurement and supply chain management.
        - Other vendors have missing or invalid bank account information, which could hinder payment processing and delay transactions.

        Examples of at-risk vendors (first 50):
        1. Inactive Suppliers:
        {inactive_suppliers_top50.to_dict()}
        2. Vendors with Invalid Bank Account Information:
        {invalid_bank_info_top50.to_dict()}

        Opportunities for Improvement:
        - If all suppliers are active, it suggests that the company is doing well in maintaining active supplier relationships. However, this also presents an opportunity to review supplier performance and assess if any suppliers might be underperforming and require more support or incentive to improve.
        - If all suppliers have valid bank accounts, it means that payment processing is less likely to encounter issues, but it is also an opportunity to revisit internal checks and validations. Consider optimizing this process or expanding it to include more detailed validation checks to prevent potential fraud or transaction errors.

        Instructions:
        1. Analyze the risk of dealing with inactive suppliers, considering the potential disruptions to supply chain operations.
        2. Suggest improvements, such as reactivating suppliers, improving supplier verification processes, or implementing stronger monitoring systems.
        3. Assess the importance of validating bank account information during the procurement process to avoid transaction delays or errors.
        """

        response = generate_response(llm_prompt)
        response = format_response(response)
        
        return chart, chart2, name, name2, response

        

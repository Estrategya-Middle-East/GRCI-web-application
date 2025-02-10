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
import numpy as np
import mpld3
import io
import base64
from datetime import timedelta, datetime
from sklearn.ensemble import IsolationForest
from django.utils.decorators import method_decorator

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
        
        # Add the user's new input
        full_prompt = prompt
        
        # Make the API request to the model
        response = requests.post(
            "http://127.0.0.1:11434/api/generate", #127.0.0.1 # ollama
            json={"model": "llama3.2:1b", "prompt": full_prompt}, # llama3.1:8b # deepseek-r1:1.5b # llama3.2:1b
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
    Formats a response to handle numbering, bulleted lists, and sentence breaks correctly.
    - Converts numbered lists (1., 2., etc.) into proper line formatting.
    - Converts `*` into sub-bullets.
    - Adds a new line after each full stop (.) or question mark (?) for better readability.
    - Adds a <br> before numbered lists (1., 2., etc.).
    - Converts **text** markers to <strong> for HTML rendering.
    """
    # Replace **text** with <strong>text</strong>
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)

    # Add a new line after full stops and question marks
    response = re.sub(r'(\:|\?)\s+', r'\1<br>', response)

    # Add a <br> before lines starting with numbers followed by a period
    response = re.sub(r'(\d+\.)', r'<br>\1', response)
    
    response = re.sub(r'(\* )', r'<br>\1', response)
    response = re.sub(r'(DeepSeek\.)', r'ESG Company.', response)
    response = re.sub(r'(DeepSeek-R1)', r'PioNeer+', response)

    lines = response.split('<br>')  # Split response into lines
    formatted_lines = []

    for line in lines:
        # Match lines starting with numbers followed by a period (e.g., 1., 2., etc.)
        if re.match(r'^\d+\.', line):
            formatted_lines.append(line)  # Add numbered line as-is
        # Match lines starting with * (sub-bullets)
        elif line.strip().startswith('*'):
            bullet = line.strip().lstrip('*').strip()
            formatted_lines.append(f"    * {bullet}")  # Indent and add bullet
        else:
            formatted_lines.append(line.strip())  # Add other lines as-is, stripping extra spaces

    return '<br>'.join(formatted_lines)



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
                response = format_response(response)

                # Save assistant response
                assistant_message = ChatMessage(role="assistant", content=response)
                assistant_message.save()

                return JsonResponse({"status": "success", "response": response})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Failed to process your message. {str(e)}"}, status=500)
        else:
            return JsonResponse({"status": "error", "message": "Invalid form submission."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


class PredictiveRiskAnalysisView(View):
    def get(self, request, *args, **kwargs):
        # Instantiate the form on GET request
        form = RiskAnalysisForm()
        return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', 
                {'form': form,
                "page_title": "Predictive Risk",
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
                'purchase_order_choices': RiskAnalysisForm.suboptions_purchase_order,
                'gl_choices': RiskAnalysisForm.suboptions_gl,})

    def post(self, request, *args, **kwargs):
        form = RiskAnalysisForm(request.POST)

        if form.is_valid():
            # Determine which button was clicked
            submit_type = request.POST.get("submit_type")  # Either "generate_graphs" or "generate_response"

            # Get the selected options
            main_category = form.cleaned_data['main_category']
            subcategory_sales_ledger = form.cleaned_data.get('subcategory_sales_ledger')
            subcategory_purchase_order = form.cleaned_data.get('subcategory_purchase_order')
            subcategory_gl = form.cleaned_data.get('subcategory_gl')

            chart = chart2 = chart3 = chart4 = None
            name = name2 = name3 = name4 = None
            response = None
            
            if main_category == 'sales_ledger':
                if subcategory_sales_ledger == 'duplicate_invoices':
                    if submit_type == "generate_graphs":
                        chart, chart2, chart3, name, name2, name3 = self.generate_duplicate_invoices_graph()
                    elif submit_type == "generate_response":
                        response = self.generate_duplicate_invoices_response()
                elif subcategory_sales_ledger == 'negative_amount':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_net_amount_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_net_amount_response()
                elif subcategory_sales_ledger == 'invalid_invoices':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_invalid_invoices_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_invalid_invoices_response()
                elif subcategory_sales_ledger == 'mismatched_subtotals':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_mismatched_subtotals_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_mismatched_subtotals_response()
                elif subcategory_sales_ledger == 'high_cash_transactions':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_high_cash_transactions_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_high_cash_transactions_response()
                elif subcategory_sales_ledger == 'unusual_prices':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_unusual_prices_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_unusual_prices_response()

            if main_category == 'purchase_order': 
                if subcategory_purchase_order == 'delayed_po_approvals':
                    if submit_type == "generate_graphs":
                        chart, chart3, name, name3 = self.generate_delayed_po_approvals_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_delayed_po_approvals_response()
                elif subcategory_purchase_order == 'open_pos':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_open_pos_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_open_pos_response()
                elif subcategory_purchase_order == 'quantity_mistmatch':
                    if submit_type == "generate_graphs":
                        chart, name = self.generate_quantity_mismatch_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_quantity_mismatch_response()
                elif subcategory_purchase_order == 'vendor_performance_risk':
                    if submit_type == "generate_graphs":
                        chart4, name4 = self.generate_vendor_performance_risk_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_vendor_performance_risk_response()
                elif subcategory_purchase_order == 'vendor_status':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.generate_vendor_status_graphs()
                    elif submit_type == "generate_response":
                        response = self.generate_vendor_status_response()
                        
            if main_category == 'general_ledger': 
                if subcategory_gl == 'reconciliation_and_balancing':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_discrepancies()
                    elif submit_type == "generate_response":
                        response = self.generate_gl_discrepancies_response()
                elif subcategory_gl == 'high_risk_transactions':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_high_risk_transactions()
                    elif submit_type == "generate_response":
                        response = self.generate_high_risk_transactions_response()
                elif subcategory_gl == 'benfords_law':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_benfords_law()
                    elif submit_type == "generate_response":
                        response = self.generate_benfords_law_response()
                elif subcategory_gl == 'cash_flow':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_cash_flow()
                    elif submit_type == "generate_response":
                        response = self.generate_cash_flow_response()
                elif subcategory_gl == 'approval_delays':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_approval_delays()
                    elif submit_type == "generate_response":
                        response = self.generate_approval_delays_response()
                elif subcategory_gl == 'department_expenses':
                    if submit_type == "generate_graphs":
                        chart2, name2 = self.plot_department_expenses()
                    elif submit_type == "generate_response":
                        response = self.generate_department_expenses_response()
                elif subcategory_gl == 'duplicate_transactions':
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = self.plot_duplicate_transactions()
                    elif submit_type == "generate_response":
                        response = self.generate_duplicate_transaction_response()

            # Pass the graphs or response to the template
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
                'gl_choices': RiskAnalysisForm.suboptions_gl,
            })
        else:
            return render(request, 'predictive_risk_analysis/predictive_risk_analysis.html', 
                {'form': form,
                "page_title": "Predictive Risk",
                'main_category_choices': RiskAnalysisForm.OPTIONS,
                'sales_ledger_choices': RiskAnalysisForm.suboptions_sales_ledger,
                'purchase_order_choices': RiskAnalysisForm.suboptions_purchase_order,
                'gl_choices': RiskAnalysisForm.suboptions_gl,})


    def load_sales_data(self):
        """ Load and preprocess sales data """
        pickle_path = "./uploads/sales_data.pkl"
        try:
            sales_data = pd.read_pickle(pickle_path)
        except Exception as e:
            raise ValueError(f"Error loading data from {pickle_path}: {str(e)}")

        sales_data.columns = [
            "branch", "branch_name", "account", "invoice", "i", "item_number", 
            "item_name", "qty_shipped", "item_price", "subtotal", "net_amount", 
            "inv_date", "reference", "cash_invoice"
        ]
        return sales_data

    def generate_duplicate_invoices_graph(self):
        """ Generate graphs for duplicate invoices analysis """
        sales_data = self.load_sales_data()
        
        # Count duplicate invoices
        invoice_counts = sales_data['invoice'].value_counts()
        duplicate_invoice_counts = invoice_counts[invoice_counts > 1]
        duplicate_invoice_summary = duplicate_invoice_counts.reset_index()
        duplicate_invoice_summary.columns = ['invoice', 'count']

        if duplicate_invoice_summary.empty:
            return None, None, None, None, None, None
        
        # Top 20 duplicate invoices (Matplotlib)
        top_20_duplicates = duplicate_invoice_summary.head(20)
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.barplot(data=top_20_duplicates, x='invoice', y='count', palette="viridis", ax=ax)
        ax.set_xlabel("Invoice Number", fontsize=12)
        ax.set_ylabel("Duplicate Count", fontsize=12)
        plt.xticks(rotation=45, ha='center')
        plt.tight_layout()
        chart3 = mpld3.fig_to_html(fig)
        name3 = "Top 20 Duplicate Invoices"

        # Top 100 duplicate invoices (Plotly)
        top_100_duplicates = duplicate_invoice_summary.head(100)
        fig_bar = px.bar(
            top_100_duplicates,
            x='invoice', 
            y='count',
            labels={'count': 'Duplicate Count', 'invoice': 'Invoice Number'},
            color='count',
            color_continuous_scale='Viridis',
            height=400,
            width=500
        )
        chart = plot.plot(fig_bar, output_type="div")
        name = "Top 100 Duplicate Invoices"

        # Duplicate vs Unique Invoices (Pie Chart)
        unique_invoices = (invoice_counts == 1).sum()
        duplicate_invoices = len(sales_data) - unique_invoices
        pie_data = pd.DataFrame({
            "Type": ["Unique Invoices", "Duplicate Invoices"],
            "Count": [unique_invoices, duplicate_invoices]
        })
        fig_pie = px.pie(
            pie_data,
            values='Count',
            names='Type',
            color='Type',
            color_discrete_map={"Unique Invoices": "blue", "Duplicate Invoices": "orange"}
        )
        chart2 = plot.plot(fig_pie, output_type="div")
        name2 = "Distribution of Duplicate vs Unique Invoices"

        return chart, chart2, chart3, name, name2, name3

    def generate_duplicate_invoices_response(self):
        """ Generate analytical response for duplicate invoices """
        sales_data = self.load_sales_data()
        
        # Count duplicate invoices
        invoice_counts = sales_data['invoice'].value_counts()
        duplicate_invoice_counts = invoice_counts[invoice_counts > 1]
        duplicate_invoice_summary = duplicate_invoice_counts.reset_index()
        duplicate_invoice_summary.columns = ['invoice', 'count']

        # Generate prompt for AI response
        if not duplicate_invoice_summary.empty:
            duplicate_invoice_text = duplicate_invoice_summary.sort_values(by='count', ascending=False).to_string(index=False)
            llm_prompt = (
                f"The following duplicate invoices were found in the dataset:\n{duplicate_invoice_text}\n\n"
                "As a business/data analyst, please analyze the implications of these duplicate invoices on business operations. "
                "Consider potential causes (e.g., system errors, data entry mistakes), and suggest practical solutions. "
                "Additionally, discuss their potential impact on financial reporting, customer trust, and operational efficiency."
            )
        else:
            llm_prompt = (
                "No duplicate invoices were found in the dataset. As a business/data analyst, please analyze the implications "
                "of having only unique invoices. Discuss positive effects on data integrity, operational efficiency, and financial reporting. "
                "Explain how maintaining unique invoices enhances trust and transparency with customers and stakeholders."
            )

        response = generate_response(llm_prompt)
        return format_response(response)
    

    # ---------------- Net Amount Graph ---------------- #
    def generate_net_amount_graphs(self):
        """ Generate graphs for net amount analysis """
        sales_data = self.load_sales_data()
        
        # Identify invoices with negative amounts
        negative_amounts = sales_data[(sales_data['subtotal'] < 0) | (sales_data['net_amount'] < 0)]
        negative_invoice_counts = negative_amounts['invoice'].value_counts().reset_index()
        negative_invoice_counts.columns = ['invoice', 'negative_count']

        # Bar Chart for Invoices with Negative Amounts
        fig_negative = px.bar(
            negative_invoice_counts,
            x='invoice',
            y='negative_count',
            labels={'negative_count': '-ve Amount Count', 'invoice': 'Invoice Number'},
            color='negative_count',
            color_continuous_scale='Viridis',
            height=400,
            width=500
        )
        chart = plot.plot(fig_negative, output_type="div")
        name = "Invoices with Negative Amounts"
        
        return chart, name

    # ---------------- Net Amount Response ---------------- #
    def generate_net_amount_response(self):
        """ Generate AI response for net amount analysis """
        sales_data = self.load_sales_data()
        negative_amounts = sales_data[(sales_data['subtotal'] < 0) | (sales_data['net_amount'] < 0)]

        num_negative_invoices = len(negative_amounts)
        llm_prompt = (
            f"The dataset contains {num_negative_invoices} invoices with negative amounts. "
            "Analyze the potential reasons for these patterns and recommend measures to prevent negative entries where applicable."
        ) if num_negative_invoices > 0 else (
            "No invoices with negative amounts were found. Confirm if further checks are needed or recommend additional areas of analysis."
        )

        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Invalid Invoices Graph ---------------- #
    def generate_invalid_invoices_graphs(self):
        """ Generate graphs for invalid invoice dates """
        sales_data = self.load_sales_data()
        
        valid_start_date = pd.Timestamp("2015-01-01")
        valid_end_date = datetime.now()

        invalid_dates = sales_data[
            (sales_data['inv_date'] < valid_start_date) | (sales_data['inv_date'] > valid_end_date)
        ]

        invalid_date_counts = invalid_dates['inv_date'].value_counts().reset_index()
        invalid_date_counts.columns = ['inv_date', 'count']
        invalid_date_counts = invalid_date_counts.sort_values(by='inv_date')

        # Line Chart for Invalid Invoice Dates
        fig_invalid_dates = px.line(
            invalid_date_counts,
            x='inv_date',
            y='count',
            labels={'inv_date': 'Invoice Date', 'count': 'Number of Invalid Entries'},
            markers=True,
            height=400,
            width=550
        )
        chart = plot.plot(fig_invalid_dates, output_type="div")
        name = "Invalid Invoice Dates Over Time"

        return chart, name

    # ---------------- Invalid Invoices Response ---------------- #
    def generate_invalid_invoices_response(self):
        """ Generate AI response for invalid invoice dates """
        sales_data = self.load_sales_data()
        valid_start_date = pd.Timestamp("2015-01-01")
        valid_end_date = datetime.now()

        invalid_dates = sales_data[
            (sales_data['inv_date'] < valid_start_date) | (sales_data['inv_date'] > valid_end_date)
        ]

        num_invalid_invoices = len(invalid_dates)
        llm_prompt = (
            f"There are {num_invalid_invoices} invoices with invalid dates. Suggest measures to mitigate such risks."
        ) if num_invalid_invoices > 0 else (
            "All invoice dates are within the valid range. Confirm if further checks are needed."
        )

        response = generate_response(llm_prompt)
        return format_response(response)
    
     # ---------------- Mismatched Subtotals Graph ---------------- #
    def generate_mismatched_subtotals_graphs(self):
        """ Generate graphs for mismatched subtotals """
        sales_data = self.load_sales_data()

        # Calculate expected subtotal
        sales_data['expected_subtotal'] = sales_data['qty_shipped'] * sales_data['item_price']
        
        # Identify mismatches where the discrepancy exceeds a tolerance
        tolerance = 0.01
        sales_data['discrepancy'] = abs(sales_data['subtotal'] - sales_data['expected_subtotal'])
        mismatched_subtotals = sales_data[sales_data['discrepancy'] > tolerance]

        # Plot histogram of subtotal discrepancies
        fig = plt.figure(figsize=(5, 4))
        plt.hist(mismatched_subtotals['discrepancy'], bins=50, color='orange', edgecolor='black')
        plt.xlabel("Discrepancy Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()

        chart = mpld3.fig_to_html(fig)
        name = "Distribution of Subtotal Discrepancies"

        return chart, name

    # ---------------- Mismatched Subtotals Response ---------------- #
    def generate_mismatched_subtotals_response(self):
        """ Generate AI response for mismatched subtotals """
        sales_data = self.load_sales_data()

        # Calculate expected subtotal
        sales_data['expected_subtotal'] = sales_data['qty_shipped'] * sales_data['item_price']
        
        # Identify mismatches where the discrepancy exceeds a tolerance
        tolerance = 0.01
        sales_data['discrepancy'] = abs(sales_data['subtotal'] - sales_data['expected_subtotal'])
        mismatched_subtotals = sales_data[sales_data['discrepancy'] > tolerance]

        num_mismatches = len(mismatched_subtotals)
        llm_prompt = (
            f"There are {num_mismatches} items with mismatched subtotals in the dataset. "
            f"These discrepancies exceed a tolerance of {tolerance}. Suggest measures to prevent such issues."
        ) if num_mismatches > 0 else (
            f"All subtotals match expected calculations within a tolerance of {tolerance}. No issues detected."
        )

        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- High Cash Transactions Graph ---------------- #
    def generate_high_cash_transactions_graphs(self):
        """ Generate graphs for high cash transactions """
        sales_data = self.load_sales_data()
        high_cash_transactions = sales_data[
            (sales_data['cash_invoice'] == 'Cash') & (sales_data['net_amount'] > 1000)
        ]
        top_50_high_cash = high_cash_transactions.nlargest(50, 'net_amount')

        # Bar Chart for High Cash Transactions
        fig = plt.figure(figsize=(5, 4))
        plt.bar(top_50_high_cash['invoice'].astype(str), top_50_high_cash['net_amount'], color='red')
        plt.xlabel('Invoice Number')
        plt.ylabel('Net Amount')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Top 50 High Cash Transactions"

        return chart, name

    # ---------------- High Cash Transactions Response ---------------- #
    def generate_high_cash_transactions_response(self):
        """ Generate AI response for high cash transactions """
        sales_data = self.load_sales_data()
        high_cash_transactions = sales_data[
            (sales_data['cash_invoice'] == 'Cash') & (sales_data['net_amount'] > 1000)
        ]

        num_high_cash = len(high_cash_transactions)
        llm_prompt = (
            f"There are {num_high_cash} high cash transactions. Discuss potential risks and control measures."
        ) if num_high_cash > 0 else (
            "No high cash transactions detected. Confirm if additional checks are required."
        )

        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Unusual Prices Graph ---------------- #
    def generate_unusual_prices_graphs(self):
        """ Generate graphs for unusual prices using anomaly detection """
        sales_data = self.load_sales_data()
        features = sales_data[['item_price', 'qty_shipped', 'net_amount']]
        model = IsolationForest(contamination=0.01, random_state=42)
        sales_data['unusual_price'] = model.fit_predict(features) == -1

        unusual_prices = sales_data[sales_data['unusual_price']]
        top_100_unusual = unusual_prices.nlargest(100, 'item_price')

        # Histogram for Unusual Prices
        fig = plt.figure(figsize=(5, 4))
        plt.hist(sales_data['item_price'], bins=50, color='lightblue', edgecolor='black', alpha=0.7)
        plt.scatter(top_100_unusual['item_price'], [0]*len(top_100_unusual), color='red', s=50, label='Unusual Prices')
        plt.xlabel('Item Price')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Unusual Prices Detected via Anomaly Detection"

        return chart, name

    # ---------------- Unusual Prices Response ---------------- #
    def generate_unusual_prices_response(self):
        """ Generate AI response for unusual price anomalies """
        sales_data = self.load_sales_data()
        unusual_prices = sales_data[sales_data['unusual_price']]

        llm_prompt = (
            "Unusual pricing anomalies were detected. Provide strategic recommendations to address risks."
        ) if not unusual_prices.empty else (
            "No pricing anomalies detected. Confirm if additional checks are needed."
        )

        response = generate_response(llm_prompt)
        return format_response(response)


    def load_po_data(self):
        """ Load and preprocess purchase order data """
        file_path = "./uploads/PO_EXTRACT.xls"
        try:
            data = pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Error loading data from {file_path}: {str(e)}")

        data['PO_CREATION_DATE'] = pd.to_datetime(data['PO_CREATION_DATE'], errors='coerce')
        data['APPROVED_DATE'] = pd.to_datetime(data['APPROVED_DATE'], errors='coerce')
        data['PO_LAST_UPDATE_DATE'] = pd.to_datetime(data.get('PO_LAST_UPDATE_DATE'), errors='coerce')
        return data

    # ---------------- Delayed PO Approvals Graph ---------------- #
    def generate_delayed_po_approvals_graphs(self):
        """ Generate graphs for delayed PO approvals """
        data = self.load_po_data()
        delay_threshold = 7

        data['Approval_Delay_Days'] = (data['APPROVED_DATE'] - data['PO_CREATION_DATE']).dt.days
        data['Delayed_Approval'] = data['Approval_Delay_Days'] > delay_threshold

        # Bar Chart: Delayed vs. On-Time Approvals
        delay_counts = data['Delayed_Approval'].value_counts()
        fig1 = plt.figure(figsize=(5, 4))
        sns.barplot(x=delay_counts.index, y=delay_counts.values, palette="viridis")
        plt.xticks([0, 1], ["On Time", "Delayed"])
        plt.xlabel("Approval Status")
        plt.ylabel("Number of POs")
        chart = mpld3.fig_to_html(fig1)
        name = "Delayed vs. On-Time PO Approvals"

        # Histogram: Distribution of Approval Delays
        fig2 = plt.figure(figsize=(5, 4))
        sns.histplot(data['Approval_Delay_Days'].dropna(), bins=30, kde=True, color='blue')
        plt.axvline(delay_threshold, color='red', linestyle='--', label="Threshold (7 Days)")
        plt.xlabel("Approval Delay (Days)")
        plt.ylabel("Number of POs")
        plt.legend()
        chart2 = mpld3.fig_to_html(fig2)
        name2 = "Distribution of PO Approval Delays"

        return chart, chart2, name, name2

    # ---------------- Delayed PO Approvals Response ---------------- #
    def generate_delayed_po_approvals_response(self):
        """ Generate AI response for delayed PO approvals """
        data = self.load_po_data()
        delay_threshold = 7

        data['Approval_Delay_Days'] = (data['APPROVED_DATE'] - data['PO_CREATION_DATE']).dt.days
        delayed_pos = data[data['Approval_Delay_Days'] > delay_threshold].nlargest(3, 'Approval_Delay_Days')
        approval_delay_min = data['Approval_Delay_Days'].min()
        approval_delay_max = data['Approval_Delay_Days'].max()

        llm_prompt = f"""
        Some POs have approval delays exceeding {delay_threshold} days, which may impact timely procurement and project delivery.
        - Examples of delayed POs: {delayed_pos[['PO_NUMBER', 'Approval_Delay_Days']].to_dict('records')}
        - Approval delay (days): {approval_delay_min}-{approval_delay_max}.

        Analyze the risk of delayed PO approvals and suggest improvements to mitigate delays.
        """
        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Open PO Graph ---------------- #
    def generate_open_pos_graphs(self):
        """ Generate graphs for open purchase orders """
        data = self.load_po_data()
        threshold_date = datetime.now() - timedelta(days=30)

        open_pos = data[data['CLOSURE_STATUS'] == 'OPEN']
        not_updated_pos = open_pos[open_pos['PO_LAST_UPDATE_DATE'].isna() | (open_pos['PO_LAST_UPDATE_DATE'] < threshold_date)]
        not_updated_pos_top50 = not_updated_pos['PO_NUMBER'].value_counts().head(50)

        # Bar Chart: Open POs Not Updated
        fig = plt.figure(figsize=(5, 4))
        plt.bar(not_updated_pos_top50.index.astype(str), not_updated_pos_top50.values, color='red')
        plt.xlabel("PO Number")
        plt.ylabel("Count of Open POs Not Updated")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Open POs Not Updated (Older than 30 Days)"

        return chart, name

    # ---------------- Open PO Response ---------------- #
    def generate_open_pos_response(self):
        """ Generate AI response for open purchase orders """
        data = self.load_po_data()
        threshold_date = datetime.now() - timedelta(days=30)

        open_pos = data[data['CLOSURE_STATUS'] == 'OPEN']
        not_updated_pos = open_pos[open_pos['PO_LAST_UPDATE_DATE'].isna() | (open_pos['PO_LAST_UPDATE_DATE'] < threshold_date)]
        not_updated_pos_top50 = not_updated_pos['PO_NUMBER'].value_counts().head(50)

        llm_prompt = f"""
        Some open POs have not been updated in over 30 days, which could indicate potential delays or unresolved issues.
        - At-risk POs: {not_updated_pos_top50.to_dict()}

        Analyze the risk of open POs that have not been updated recently, and suggest process improvements.
        """
        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Quantity Mismatch Graph ---------------- #
    def generate_quantity_mismatch_graphs(self):
        """ Generate graphs for quantity mismatches """
        data = self.load_po_data()

        data['Quantity_Mismatch'] = data['QUANTITY'] - data['QUANTITY_RECEIVED'] - data['QUANTITY_CANCELLED']
        significant_mismatches = data[(data['Quantity_Mismatch'] > 10) | (data['Quantity_Mismatch'] > 0.2 * data['QUANTITY'])]
        top_mismatches = significant_mismatches.nlargest(50, 'Quantity_Mismatch')

        # Bar Chart: Quantity Mismatches
        fig = plt.figure(figsize=(5, 4))
        plt.bar(top_mismatches['PO_NUMBER'].astype(str), top_mismatches['Quantity_Mismatch'], color='red')
        plt.xlabel("Purchase Order Numbers")
        plt.ylabel("Quantity Mismatch (Units)")
        plt.xticks(rotation=45, fontsize=9)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Top Significant Quantity Mismatches Across Purchase Orders"

        return chart, name

    # ---------------- Quantity Mismatch Response ---------------- #
    def generate_quantity_mismatch_response(self):
        """ Generate AI response for quantity mismatches """
        data = self.load_po_data()

        data['Quantity_Mismatch'] = data['QUANTITY'] - data['QUANTITY_RECEIVED'] - data['QUANTITY_CANCELLED']
        significant_mismatches = data[(data['Quantity_Mismatch'] > 10) | (data['Quantity_Mismatch'] > 0.2 * data['QUANTITY'])]
        top_mismatched_pos = significant_mismatches.nlargest(50, 'Quantity_Mismatch')

        llm_prompt = f"""
        Some POs have significant mismatches between ordered and received quantities. This may indicate supplier performance issues or inventory problems.
        - Examples of mismatched POs: {top_mismatched_pos[['PO_NUMBER', 'Quantity_Mismatch']].to_dict('records')}

        Analyze the risk of quantity mismatches and suggest process improvements.
        """
        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Vendor Performance Risk Graph ---------------- #
    def generate_vendor_performance_risk_graphs(self):
        """ Generate graphs for vendor performance risks """
        data = self.load_po_data()

        # Calculate Quantity Mismatch
        data['Quantity_Mismatch'] = data['QUANTITY'] - data['QUANTITY_RECEIVED']

        # Identify vendors with high cancellation rates
        data['Cancellation_Rate'] = data['QUANTITY_CANCELLED'] / data['QUANTITY']
        high_cancellation_vendors = data[data['Cancellation_Rate'] > 0.2]

        # Top Vendors by Quantity Mismatch
        vendor_mismatch = data.groupby('VENDOR_NAME')['Quantity_Mismatch'].sum()
        top_vendors_by_mismatch = vendor_mismatch.sort_values(ascending=False).head(10)

        # Plot Vendor Risk Analysis
        fig = plt.figure(figsize=(12, 8))

        # Bar chart for high cancellation rates
        plt.subplot(1, 2, 1)
        high_cancellation_vendors_grouped = high_cancellation_vendors.groupby('VENDOR_NAME')['Cancellation_Rate'].mean().sort_values(ascending=False)
        plt.bar(high_cancellation_vendors_grouped.index, high_cancellation_vendors_grouped.values, color='orange')
        plt.title("Vendors with High Cancellation Rates (>20%)")
        plt.ylabel("Cancellation Rate")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()

        # Bar chart for top vendors by quantity mismatch
        plt.subplot(1, 2, 2)
        plt.bar(top_vendors_by_mismatch.index, top_vendors_by_mismatch.values, color='red')
        plt.title("Top 10 Vendors by Quantity Mismatch")
        plt.ylabel("Total Quantity Mismatch (Units)")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()

        chart = mpld3.fig_to_html(fig)
        name = "Vendor Performance Risk Analysis"

        return chart, name

    # ---------------- Vendor Performance Risk Response ---------------- #
    def generate_vendor_performance_risk_response(self):
        """ Generate AI response for vendor performance risks """
        data = self.load_po_data()

        # Identify vendors with high cancellation rates
        data['Cancellation_Rate'] = data['QUANTITY_CANCELLED'] / data['QUANTITY']
        high_cancellation_vendors = data[data['Cancellation_Rate'] > 0.2]

        # Top Vendors by Quantity Mismatch
        vendor_mismatch = data.groupby('VENDOR_NAME')['Quantity_Mismatch'].sum()
        top_vendors_by_mismatch = vendor_mismatch.sort_values(ascending=False).head(10)

        llm_prompt = f"""
        Some vendors have high cancellation rates (>20%) and significant quantity mismatches. This may indicate supply chain inefficiencies or supplier performance risks.
        - High Cancellation Rate Vendors: {high_cancellation_vendors[['VENDOR_NAME', 'Cancellation_Rate']].to_dict('records')}
        - Top 10 Vendors by Quantity Mismatch: {top_vendors_by_mismatch.to_dict()}

        Analyze the risks associated with vendor performance and suggest process improvements.
        """
        response = generate_response(llm_prompt)
        return format_response(response)

    # ---------------- Vendor Status Graph ---------------- #
    def generate_vendor_status_graphs(self):
        """ Generate graphs for vendor status risks """
        data = self.load_po_data()

        # Identify inactive suppliers
        inactive_suppliers = data[data['SUPPLIER_STATUS'] != 'Active']
        inactive_suppliers_top50 = inactive_suppliers['VENDOR_NAME'].value_counts().head(50)

        # Identify vendors with invalid bank information
        invalid_bank_info = data[data['BANK ACCOUNT NUMBER'].isna() | data['BANK ACCOUNT NAME'].isna()]
        invalid_bank_info_top50 = invalid_bank_info['VENDOR_NAME'].value_counts().head(50)

        # Bar Chart: Inactive Suppliers
        fig = plt.figure(figsize=(5, 4))
        plt.bar(inactive_suppliers_top50.index, inactive_suppliers_top50.values, color='red')
        plt.title("Inactive Suppliers")
        plt.xlabel("Vendor Name")
        plt.ylabel("Count of Inactive Suppliers")
        plt.xticks(rotation=45, ha='right', fontsize=7)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Inactive Suppliers"

        # Bar Chart: Vendors with Invalid Bank Info
        fig2 = plt.figure(figsize=(5, 6))
        plt.bar(invalid_bank_info_top50.index, invalid_bank_info_top50.values, color='red')
        plt.title("Vendors with Invalid Bank Information")
        plt.xlabel("Vendor Name")
        plt.ylabel("Count of Invalid Bank Accounts")
        plt.xticks(rotation=45, ha='right', fontsize=7)
        plt.tight_layout()
        chart2 = mpld3.fig_to_html(fig2)
        name2 = "Vendors with Invalid Bank Information"

        return chart, chart2, name, name2

    # ---------------- Vendor Status Response ---------------- #
    def generate_vendor_status_response(self):
        """ Generate AI response for vendor status risks """
        data = self.load_po_data()

        # Identify inactive suppliers
        inactive_suppliers = data[data['SUPPLIER_STATUS'] != 'Active']
        inactive_suppliers_top50 = inactive_suppliers['VENDOR_NAME'].value_counts().head(50)

        # Identify vendors with invalid bank information
        invalid_bank_info = data[data['BANK ACCOUNT NUMBER'].isna() | data['BANK ACCOUNT NAME'].isna()]
        invalid_bank_info_top50 = invalid_bank_info['VENDOR_NAME'].value_counts().head(50)

        llm_prompt = f"""
        Some suppliers are marked as inactive, and others have missing or invalid bank account information.
        - Inactive Suppliers: {inactive_suppliers_top50.to_dict()}
        - Vendors with Invalid Bank Account Information: {invalid_bank_info_top50.to_dict()}

        Analyze the risks of inactive suppliers and missing payment details and suggest process improvements.
        """
        response = generate_response(llm_prompt)
        return format_response(response)
    
######################################
    def load_gl_data(self):
        """ Load and preprocess General Ledger (GL) data """
        file_path = "./uploads/GL data in Audit format.xls"
        try:
            gl_data = pd.read_excel(file_path, engine='xlrd')
        except Exception as e:
            raise ValueError(f"Error loading data from {file_path}: {str(e)}")

        gl_data.columns = [
            "sr", "accounting_year", "document_date", "transaction_code", "document_number",
            "sequence_number", "document_reference", "main_account_code", "main_account_name",
            "sub_account_code", "sub_account_name", "division_code", "department_code",
            "analysis_code", "currency_code", "debit_credit_flag", "document_amount",
            "description", "created_user", "created_date", "approved_user", "approved_date"
        ]
        return gl_data

    def reconcile_gl_balances(self):
        """ Identify discrepancies between total debits and credits per day """
        gl_data = self.load_gl_data()

        # Ensure document date is in datetime format
        gl_data['document_date'] = pd.to_datetime(gl_data['document_date'], errors='coerce')

        # Separate debit and credit transactions
        gl_data['debit'] = gl_data.apply(lambda x: x['document_amount'] if x['debit_credit_flag'] == 'D' else 0, axis=1)
        gl_data['credit'] = gl_data.apply(lambda x: x['document_amount'] if x['debit_credit_flag'] == 'C' else 0, axis=1)

        # Aggregate daily balances
        daily_balances = gl_data.groupby("document_date")[["debit", "credit"]].sum()

        # Identify discrepancies where debits != credits
        discrepancies = daily_balances[daily_balances["debit"] != daily_balances["credit"]]

        return discrepancies

    def plot_discrepancies(self):
        """ Generate visualization for discrepancies """
        discrepancies = self.reconcile_gl_balances()

        if discrepancies.empty:
            return "No discrepancies found.", "No discrepancies found.", "No discrepancies found.", "No discrepancies found."

        # Matplotlib Bar Chart - Discrepancy Amounts
        fig, ax = plt.subplots(figsize=(6, 4))
        discrepancies.plot(kind="bar", ax=ax)
        ax.set_title("Daily Debit vs Credit Discrepancies")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount Difference")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "GL Reconciliation Discrepancies"

        # Plotly Chart - Discrepancy Over Time
        fig_plotly = px.bar(
            discrepancies.reset_index(),
            x="document_date",
            y=["debit", "credit"],
            title="Daily Debit vs Credit Discrepancies",
            labels={"value": "Amount", "variable": "Transaction Type"},
            color_discrete_map={"debit": "red", "credit": "green"},
            barmode="group"
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "GL Discrepancy Trend"

        return chart, chart2, name, name2   
    
    def generate_gl_discrepancies_response(self):
        """ Generate AI-powered analytical response for GL reconciliation discrepancies """
        discrepancies = self.reconcile_gl_balances()

        # Generate prompt for AI analysis
        if not discrepancies.empty:
            discrepancy_text = discrepancies.sort_values(by="debit", ascending=False).to_string(index=True)
            llm_prompt = (
                f"The following discrepancies were found in the General Ledger reconciliation:\n{discrepancy_text}\n\n"
                "As a business/data analyst, please analyze the implications of these debit-credit imbalances. "
                "Consider potential causes such as missing transactions, incorrect data entries, timing differences, or system errors. "
                "Additionally, suggest solutions to ensure better reconciliation and discuss the impact on financial reporting, "
                "audit compliance, and internal controls."
            )
        else:
            llm_prompt = (
                "No discrepancies were found in the General Ledger reconciliation. As a business/data analyst, "
                "please analyze the positive implications of maintaining a well-balanced ledger. "
                "Discuss how accurate financial reconciliation enhances data integrity, regulatory compliance, and financial stability. "
                "Additionally, suggest best practices to maintain accurate debit-credit matching."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed

  
    def identify_high_risk_transactions(self, threshold=1000000):
        """ Identify high-risk transactions exceeding a defined threshold """
        gl_data = self.load_gl_data()

        # Filter high-risk transactions
        high_risk = gl_data[gl_data["document_amount"] > threshold]

        return high_risk

    def plot_high_risk_transactions(self, threshold=1000000):
        """ Generate graphs for high-risk transactions """
        high_risk = self.identify_high_risk_transactions(threshold)

        if high_risk.empty:
            return "No high-risk transactions found.", "No high-risk transactions found.", "No high-risk transactions found.", "No high-risk transactions found."

        # Matplotlib Bar Chart - High-Risk Transaction Amounts
        fig, ax = plt.subplots(figsize=(6, 4))
        high_risk.plot(kind="bar", x="document_number", y="document_amount", ax=ax, color='red')
        ax.set_title(f"High-Risk Transactions (>{threshold})")
        ax.set_xlabel("Document Number")
        ax.set_ylabel("Transaction Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "High-Risk Transactions"

        # Plotly Chart - Distribution of High-Risk Transactions
        fig_plotly = px.histogram(
            high_risk,
            x="document_amount",
            nbins=20,
            title=f"Distribution of High-Risk Transactions (>{threshold})",
            labels={"document_amount": "Transaction Amount"},
            color_discrete_sequence=["red"]
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "High-Risk Transaction Distribution"

        return chart, chart2, name, name2
    
    def generate_high_risk_transactions_response(self, threshold=1000000):
        """ Generate AI-powered analytical response for high-risk transactions """
        high_risk = self.identify_high_risk_transactions(threshold)

        # Generate prompt for AI analysis
        if not high_risk.empty:
            high_risk_text = high_risk.sort_values(by="document_amount", ascending=False).to_string(index=False)
            llm_prompt = (
                f"The following high-risk transactions were identified (Threshold: {threshold}):\n{high_risk_text}\n\n"
                "As a business/data analyst, please analyze the implications of these high-value transactions. "
                "Consider potential risks such as fraud, unauthorized expenses, accounting errors, or financial mismanagement. "
                "Additionally, suggest risk mitigation strategies, including approval workflows, audit reviews, and anomaly detection models."
            )
        else:
            llm_prompt = (
                f"No high-risk transactions were found exceeding {threshold}. "
                "As a business/data analyst, please discuss the benefits of having controlled transaction amounts. "
                "Explain how maintaining strict financial thresholds helps in minimizing risks, ensuring compliance, and improving financial integrity."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed

   
    
    def plot_benfords_law(self):
        """ Analyze journal entries for compliance with Benford's Law """
        gl_data = self.load_gl_data()

        # Extract first digits from document amounts
        gl_data["first_digit"] = gl_data["document_amount"].astype(str).str[0]
        leading_digits = gl_data["first_digit"].value_counts(normalize=True).sort_index()

        # Expected Benford’s Law Distribution
        benford_distribution = np.log10(1 + 1 / np.arange(1, 10))

        # Matplotlib Bar Chart - Actual vs Benford’s Law
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(leading_digits.index.astype(int), leading_digits.values, color='blue', alpha=0.7, label="Actual Data")
        ax.plot(np.arange(1, 10), benford_distribution, marker="o", linestyle="dashed", color="red", label="Benford's Law")
        ax.set_title("Benford’s Law Compliance")
        ax.set_xlabel("First Digit")
        ax.set_ylabel("Frequency")
        ax.legend()
        plt.xticks(np.arange(1, 10))
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Benford’s Law Compliance"

        # Plotly Chart - Benford's Distribution
        df_benford = pd.DataFrame({"First Digit": np.arange(1, 10), "Expected": benford_distribution})
        df_actual = pd.DataFrame({"First Digit": leading_digits.index.astype(int), "Actual": leading_digits.values})

        fig_plotly = px.bar(
            df_actual,
            x="First Digit",
            y="Actual",
            title="Benford’s Law - Actual vs Expected",
            labels={"Actual": "Observed Frequency"},
            color="First Digit"
        )
        fig_plotly.add_scatter(x=df_benford["First Digit"], y=df_benford["Expected"], mode='lines', name="Benford's Law")
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "Benford’s Law - Actual vs Expected"

        return chart, chart2, name, name2
    
    def generate_benfords_law_response(self):
        """ Generate AI-powered analytical response for Benford’s Law anomalies """
        gl_data = self.load_gl_data()

        # Extract first digits from document amounts
        # Ensure only digits 1-9 are considered
        gl_data["first_digit"] = gl_data["document_amount"].astype(str).str[0]
        gl_data = gl_data[gl_data["first_digit"].isin([str(i) for i in range(1, 10)])]  # Remove '0'

        # Compute actual first-digit frequencies
        leading_digits = gl_data["first_digit"].value_counts(normalize=True).sort_index()

        # Expected Benford’s Law Distribution
        benford_distribution = np.log10(1 + 1 / np.arange(1, 10))

        # Ensure arrays match before computing deviations
        if len(leading_digits) != len(benford_distribution):
            raise ValueError(f"Data mismatch: leading_digits({len(leading_digits)}) vs benford_distribution({len(benford_distribution)})")

        # Calculate deviation
        deviations = leading_digits - benford_distribution

        deviation_text = deviations.to_string(index=True)

        # Generate AI Analysis Prompt
        llm_prompt = (
            f"The following deviations from Benford’s Law were observed in the journal entries:\n{deviation_text}\n\n"
            "As a business/data analyst, analyze the potential risks associated with these anomalies. "
            "Discuss whether these deviations may indicate fraudulent transactions, data manipulation, or reporting errors. "
            "Additionally, suggest audit strategies to investigate these anomalies and recommend controls to mitigate financial risks."
        )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed

    def analyze_cash_flow(self):
        """ Categorize cash inflows and outflows by account type """
        gl_data = self.load_gl_data()

        # Aggregate inflows (Credits) and outflows (Debits)
        cash_flow = gl_data.groupby(["main_account_name", "debit_credit_flag"])["document_amount"].sum().unstack(fill_value=0)

        # Ensure correct mapping based on available columns
        column_mapping = {}
        if "D" in cash_flow.columns:
            column_mapping["D"] = "Cash Outflow"
        if "C" in cash_flow.columns:
            column_mapping["C"] = "Cash Inflow"

        # Rename columns
        cash_flow.rename(columns=column_mapping, inplace=True)

        # Ensure missing inflow/outflow columns are added with 0 values
        if "Cash Inflow" not in cash_flow.columns:
            cash_flow["Cash Inflow"] = 0
        if "Cash Outflow" not in cash_flow.columns:
            cash_flow["Cash Outflow"] = 0

        # Calculate Net Cash Flow
        cash_flow["Net Cash Flow"] = cash_flow["Cash Inflow"] - cash_flow["Cash Outflow"]

        return cash_flow


    def plot_cash_flow(self):
        """ Generate visual analysis of cash flow categorization """
        cash_flow = self.analyze_cash_flow()  # ✅ Use processed cash flow, not raw GL data

        if cash_flow.empty:
            return "No cash flow data available.", "No cash flow data available.", "No cash flow data available.", "No cash flow data available."

        # Debugging: Ensure expected columns exist
        print("Cash Flow Columns:", cash_flow.columns)

        # Ensure Cash Inflow and Cash Outflow columns exist before plotting
        required_columns = ["Cash Inflow", "Cash Outflow"]
        for col in required_columns:
            if col not in cash_flow.columns:
                cash_flow[col] = 0  # Fill missing columns with zeros

        # Matplotlib Bar Chart - Cash Inflows and Outflows
        fig, ax = plt.subplots(figsize=(8, 5))
        cash_flow[["Cash Inflow", "Cash Outflow"]].plot(kind="bar", stacked=True, ax=ax)
        ax.set_title("Cash Flow Categorization by Account")
        ax.set_xlabel("Main Account Name")
        ax.set_ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Cash Flow Categorization"

        # Plotly Chart - Net Cash Flow per Account
        fig_plotly = px.bar(
            cash_flow.reset_index(),
            x="main_account_name",
            y="Net Cash Flow",
            title="Net Cash Flow by Account",
            labels={"Net Cash Flow": "Amount", "main_account_name": "Account Name"},
            color="Net Cash Flow",
            color_continuous_scale="Viridis"
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "Net Cash Flow by Account"

        return chart, chart2, name, name2


    def generate_cash_flow_response(self):
        """ Generate AI-powered analytical response for cash flow analysis """
        cash_flow = self.analyze_cash_flow()

        # Generate AI analysis prompt
        if not cash_flow.empty:
            cash_flow_text = cash_flow.to_string(index=True)
            llm_prompt = (
                f"The following cash flow distribution was observed:\n{cash_flow_text}\n\n"
                "As a financial analyst, analyze the implications of the cash inflows and outflows. "
                "Discuss liquidity risks, dependency on specific revenue sources, and potential inefficiencies in cash management. "
                "Additionally, suggest strategies for improving cash flow stability, optimizing expenditures, and ensuring financial resilience."
            )
        else:
            llm_prompt = (
                "No significant cash flow data is available. As a financial analyst, "
                "please discuss the importance of tracking cash inflows and outflows. "
                "Explain how proper liquidity management impacts business sustainability, risk mitigation, and operational efficiency."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed
    def analyze_approval_delays(self, threshold=5):
        """ Calculate approval delays and identify delayed transactions """
        gl_data = self.load_gl_data()

        # Ensure dates are in datetime format
        gl_data["created_date"] = pd.to_datetime(gl_data["created_date"], errors="coerce")
        gl_data["approved_date"] = pd.to_datetime(gl_data["approved_date"], errors="coerce")

        # Calculate approval delay in days
        gl_data["approval_delay_days"] = (gl_data["approved_date"] - gl_data["created_date"]).dt.days

        # Filter transactions with delays beyond the threshold
        delayed_transactions = gl_data[gl_data["approval_delay_days"] > threshold]

        return delayed_transactions

    def plot_approval_delays(self, threshold=5):
        """ Generate visual analysis of transaction approval delays """
        delayed_transactions = self.analyze_approval_delays(threshold)

        if delayed_transactions.empty:
            return "No approval delays found.", "No approval delays found.", "No approval delays found.", "No approval delays found."

        # Matplotlib Histogram - Approval Delays Distribution
        fig, ax = plt.subplots(figsize=(8, 5))
        delayed_transactions["approval_delay_days"].hist(bins=20, ax=ax, color="red", alpha=0.7)
        ax.set_title(f"Approval Delay Distribution (>{threshold} Days)")
        ax.set_xlabel("Approval Delay (Days)")
        ax.set_ylabel("Number of Transactions")
        plt.tight_layout()
        chart = mpld3.fig_to_html(fig)
        name = "Approval Delay Distribution"

        # Plotly Box Plot - Approval Delay Trends
        fig_plotly = px.box(
            delayed_transactions,
            x="department_code",
            y="approval_delay_days",
            title="Approval Delay by Department",
            labels={"approval_delay_days": "Approval Delay (Days)", "department_code": "Department"},
            color="department_code"
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "Approval Delay by Department"

        return chart, chart2, name, name2
    
    def generate_approval_delays_response(self, threshold=5):
        """ Generate AI-powered analytical response for approval delay analysis """
        delayed_transactions = self.analyze_approval_delays(threshold)

        # Generate AI analysis prompt
        if not delayed_transactions.empty:
            delay_summary = delayed_transactions.groupby("department_code")["approval_delay_days"].mean().round(2).to_string()
            llm_prompt = (
                f"The following approval delays were observed (Threshold: {threshold} days):\n{delay_summary}\n\n"
                "As a business/data analyst, analyze the implications of these approval delays. "
                "Discuss how delays in transaction approval impact cash flow, project execution, and vendor relationships. "
                "Additionally, suggest strategies to optimize workflow efficiency and reduce approval bottlenecks."
            )
        else:
            llm_prompt = (
                f"No significant approval delays beyond {threshold} days were found. "
                "As a business/data analyst, discuss the benefits of an efficient approval process. "
                "Explain how reducing bottlenecks in approval workflows improves financial planning, operational efficiency, and stakeholder satisfaction."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed

    def analyze_department_expenses(self):
        """ Analyze expenses incurred by different departments """
        gl_data = self.load_gl_data()

        # Filter transactions containing "Expense" in the Main Account Name
        expense_trans = gl_data[gl_data["main_account_name"].str.contains("Expense", na=False, case=False)]

        # Summarize total expenses by department
        expenses_by_dept = expense_trans.groupby("department_code")["document_amount"].sum().reset_index()

        return expenses_by_dept

        
    def plot_department_expenses(self):
        """ Generate visual analysis of expenses by department """
        expenses_by_dept = self.analyze_department_expenses()

        if expenses_by_dept.empty:
            return None, "No expense data available."


        # Plotly Chart - Expense Distribution
        fig_plotly = px.pie(
            expenses_by_dept,
            names="department_code",
            values="document_amount",
            title="Expense Distribution by Department",
            labels={"document_amount": "Total Expense", "department_code": "Department"},
            color_discrete_sequence=px.colors.sequential.Redor
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "Expense Distribution by Department"

        return chart2, name2

    
    def generate_department_expenses_response(self):
        """ Generate AI-powered analytical response for department expense analysis """
        expenses_by_dept = self.analyze_department_expenses()

        # Generate AI analysis prompt
        if not expenses_by_dept.empty:
            expense_summary = expenses_by_dept.sort_values(by="document_amount", ascending=False).to_string(index=False)
            llm_prompt = (
                f"The following department-wise expense distribution was observed:\n{expense_summary}\n\n"
                "As a financial analyst, analyze the implications of departmental spending. "
                "Discuss whether high expenditures in specific departments indicate necessary investments, mismanagement, or budget overruns. "
                "Additionally, suggest strategies to control spending, optimize budgets, and ensure financial alignment with company goals."
            )
        else:
            llm_prompt = (
                "No significant department-wise expenses were found. "
                "As a financial analyst, discuss the importance of tracking departmental expenditures. "
                "Explain how monitoring expenses improves financial discipline, budget adherence, and operational efficiency."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed
    
    def detect_duplicate_transactions(self):
        """ Identify duplicate transactions based on Document Number, Date, and Amount """
        gl_data = self.load_gl_data()

        # Find duplicate transactions
        duplicates = gl_data[gl_data.duplicated(["document_number", "document_date", "document_amount"], keep=False)]

        return duplicates
    
    def plot_duplicate_transactions(self):
        """ Generate visual analysis of duplicate transactions """
        duplicates = self.detect_duplicate_transactions()

        if duplicates.empty:
            return None, None, "No duplicate transactions found."

        # Count duplicates by date
        duplicate_counts = duplicates.groupby("document_date")["document_number"].count().reset_index()

        # Matplotlib Bar Chart - Duplicate Transactions Over Time
        fig, ax = plt.subplots(figsize=(8, 5))
        duplicate_counts.plot(kind="bar", x="document_date", y="document_number", ax=ax, color="orange")
        ax.set_title("Duplicate Transactions Over Time")
        ax.set_xlabel("Document Date")
        ax.set_ylabel("Number of Duplicates")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart1 = mpld3.fig_to_html(fig)
        name1 = "Duplicate Transactions Timeline"

        # Plotly Chart - Top 10 Most Frequent Duplicates
        top_duplicates = duplicates.groupby(["document_number", "document_amount"]).size().reset_index(name="count")
        top_duplicates = top_duplicates.sort_values(by="count", ascending=False).head(10)

        fig_plotly = px.bar(
            top_duplicates,
            x="document_number",
            y="count",
            title="Top 10 Duplicate Transactions",
            labels={"count": "Duplicate Count", "document_number": "Document Number"},
            color="count",
            color_continuous_scale="Oranges"
        )
        chart2 = plot.plot(fig_plotly, output_type="div")
        name2 = "Top 10 Duplicate Transactions"

        return chart1, chart2, name1, name2
    
    def generate_duplicate_transaction_response(self):
        """ Generate AI-powered analytical response for duplicate transactions """
        duplicates = self.detect_duplicate_transactions()

        # Generate AI analysis prompt
        if not duplicates.empty:
            duplicate_summary = duplicates.groupby("document_number")["document_amount"].count().to_string()
            llm_prompt = (
                f"The following duplicate transactions were identified:\n{duplicate_summary}\n\n"
                "As a financial analyst, analyze the risks associated with duplicate transactions. "
                "Discuss how these duplicates could lead to overpayments, financial reporting inaccuracies, or fraud risks. "
                "Additionally, suggest corrective actions such as process automation, validation controls, and auditing mechanisms to prevent duplicates."
            )
        else:
            llm_prompt = (
                "No duplicate transactions were detected. "
                "As a financial analyst, discuss the importance of preventing duplicate transactions. "
                "Explain how maintaining unique transactions improves financial accuracy, reduces risks, and ensures proper financial controls."
            )

        # Generate AI response (replace with actual AI function)
        response = generate_response(llm_prompt)  # Replace with actual AI call
        return format_response(response)  # Replace with formatting function if needed
        
######################################
class PredictiveRiskOptionsAPI(View):
    def get(self, request, *args, **kwargs):
        options = {
            "main_categories": RiskAnalysisForm.OPTIONS,
            "sales_ledger_subcategories": RiskAnalysisForm.suboptions_sales_ledger,
            "purchase_order_subcategories": RiskAnalysisForm.suboptions_purchase_order,
        }
        return JsonResponse({"status": "success", "data": options})
    

@method_decorator(csrf_exempt, name='dispatch')
class PredictiveRiskAnalysisAPI(View):
    def post(self, request, *args, **kwargs):
        try:
            print("🔍 Headers:", request.headers)
            print("🔍 Raw request body (decoded):", request.body.decode("utf-8"))

            # Parse JSON request body
            data = json.loads(request.body.decode("utf-8"))

            # Extract parameters
            main_category = data.get("main_category")
            subcategory = data.get("subcategory")
            submit_type = data.get("submit_type")

            # Validate input
            if not main_category or not subcategory or not submit_type:
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            # Create an instance of the existing class to reuse its methods
            risk_analysis = PredictiveRiskAnalysisView()

            chart = chart2 = chart3 = chart4 = None
            name = name2 = name3 = name4 = None
            response = None

            # Sales Ledger Cases
            if main_category == "sales_ledger":
                if subcategory == "duplicate_invoices":
                    if submit_type == "generate_graphs":
                        chart, chart2, chart3, name, name2, name3 = risk_analysis.generate_duplicate_invoices_graph()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_duplicate_invoices_response()

                elif subcategory == "negative_amount":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_net_amount_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_net_amount_response()

                elif subcategory == "invalid_invoices":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_invalid_invoices_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_invalid_invoices_response()

                elif subcategory == "mismatched_subtotals":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_mismatched_subtotals_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_mismatched_subtotals_response()

                elif subcategory == "high_cash_transactions":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_high_cash_transactions_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_high_cash_transactions_response()

                elif subcategory == "unusual_prices":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_unusual_prices_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_unusual_prices_response()

            # Purchase Order Cases
            elif main_category == "purchase_order":
                if subcategory == "delayed_po_approvals":
                    if submit_type == "generate_graphs":
                        chart, chart3, name, name3 = risk_analysis.generate_delayed_po_approvals_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_delayed_po_approvals_response()

                elif subcategory == "open_pos":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_open_pos_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_open_pos_response()

                elif subcategory == "quantity_mistmatch":
                    if submit_type == "generate_graphs":
                        chart, name = risk_analysis.generate_quantity_mismatch_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_quantity_mismatch_response()

                elif subcategory == "vendor_performance_risk":
                    if submit_type == "generate_graphs":
                        chart4, name4 = risk_analysis.generate_vendor_performance_risk_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_vendor_performance_risk_response()

                elif subcategory == "vendor_status":
                    if submit_type == "generate_graphs":
                        chart, chart2, name, name2 = risk_analysis.generate_vendor_status_graphs()
                    elif submit_type == "generate_response":
                        response = risk_analysis.generate_vendor_status_response()

            # Return JSON response
            if submit_type == "generate_graphs":
                return JsonResponse({
                    "charts": {
                        "chart1": chart,
                        "chart2": chart2,
                        "chart3": chart3,
                        "chart4": chart4
                    },
                    "names": {
                        "chart1_name": name,
                        "chart2_name": name2,
                        "chart3_name": name3,
                        "chart4_name": name4
                    },
                    "message": f"{subcategory.replace('_', ' ').title()} graphs generated successfully"
                })

            elif submit_type == "generate_response":
                return JsonResponse({"analysis": response})

            return JsonResponse({"error": "Invalid request parameters"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

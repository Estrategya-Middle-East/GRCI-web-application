from django import forms

class ChatInputForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Type your message...', 'class': 'form-control'}
        )
    )



class RiskAnalysisForm(forms.Form):
    OPTIONS = [
        ('sales_ledger', 'Sales Ledger'),
        ('purchase_order', 'Purchase Order'),
        ('budgets_forecasts', 'Budgets and Forecasts'),
        ('project_schedules', 'Project Schedules and Gantt Charts'),
        ('stakeholder_analysis', 'Stakeholder Analysis'),
        ('production_schedules', 'Production Schedules'),
        ('employee_records', 'Employee Records')
    ]

    suboptions_sales_ledger = [
        ('duplicate_invoices', 'Duplicate Invoices'),
        ('invalid_invoices', 'Invalid Invoices'),
        ('negative_amount', 'Negative Amount'),
        ('mismatched_subtotals', 'Mismatched Subtotals'),
        ('high_cash_transactions', 'High Cash Transactions'),
        ('unusual_prices', 'Unusual Prices'),
        
    ]
    
    suboptions_purchase_order = [
        ('delayed_po_approvals', 'Delayed PO Approvals'),
        ('open_pos', 'OPEN POs'),
        ('quantity_mistmatch', 'Quantity Mistmatch'),
        ('vendor_performance_risk', 'Vendor Performance Risk'),
        ('vendor_status', 'Vendor Status'),
        
    ]

    main_category = forms.ChoiceField(choices=OPTIONS, label="Select Risk Category")
    subcategory_sales_ledger = forms.ChoiceField(choices=suboptions_sales_ledger, label="Select Subcategory", required=False)
    subcategory_purchase_order = forms.ChoiceField(choices=suboptions_purchase_order, label="Select Subcategory", required=False)

    def clean(self):
        cleaned_data = super().clean()
        main_category = cleaned_data.get('main_category')

        # Make sure subcategory is only required for Sales Ledger
        if main_category == 'sales_ledger':
            self.fields['subcategory_sales_ledger'].required = True
        else:
            self.fields['subcategory_sales_ledger'].required = False
        
        if main_category == 'purchase_order':
            self.fields['subcategory_purchase_order'].required = True
        else:
            self.fields['subcategory_purchase_order'].required = False

        return cleaned_data

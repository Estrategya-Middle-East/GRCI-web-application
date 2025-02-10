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
        ('general_ledger', 'General Ledger'),
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
    suboptions_gl = [
        ('reconciliation_and_balancing', 'GL Reconciliation and Balancing'),
        ('high_risk_transactions', 'High-Risk Transaction Identification'),
        ('benfords_law', 'Benford’s Law '),
        ('cash_flow', 'Cash Flow Categorization and Analysis'),
        ('approval_delays', 'Transaction Approval Delay Analysis'),
        ('department_expenses', 'Expense Analysis by Department'),
        ('duplicate_transactions', 'Duplicate Transaction Detection'),
    ]
    
    main_category = forms.ChoiceField(choices=OPTIONS, label="Select Risk Category")
    subcategory_sales_ledger = forms.ChoiceField(choices=suboptions_sales_ledger, label="Select Subcategory", required=False)
    subcategory_purchase_order = forms.ChoiceField(choices=suboptions_purchase_order, label="Select Subcategory", required=False)
    subcategory_gl = forms.ChoiceField(choices=suboptions_gl, label="Select Subcategory", required=False)

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
            
        if main_category == 'general_ledger':
            self.fields['subcategory_gl'].required = True
        else:
            self.fields['subcategory_gl'].required = False

        return cleaned_data

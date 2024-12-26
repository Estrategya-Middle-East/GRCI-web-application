from django.shortcuts import render

# Create your views here.
# ISM Dashboard View
def dashboard(request):
    components = [
        {"name": "Governance and Leadership", "icon": "fas fa-users-cog", "link": "#"},  # Users cog for leadership and governance
        {"name": "Risk Assessment and Management", "icon": "fas fa-clipboard-list", "link": "#"},  # Clipboard list for risk assessment
        {"name": "Asset Management", "icon": "fas fa-archive", "link": "#"},  # Archive for asset management
        {"name": "Access Control", "icon": "fas fa-lock", "link": "#"},  # Lock for access control
        {"name": "Incident Management", "icon": "fas fa-exclamation-triangle", "link": "#"},  # Exclamation triangle for incidents
        {"name": "Business Continuity and Recovery", "icon": "fas fa-recycle", "link": "#"},  # Recycle for continuity and recovery
        {"name": "Supplier and Third-Party Management", "icon": "fas fa-handshake", "link": "#"},  # Handshake for suppliers and third parties
        {"name": "Awareness and Training", "icon": "fas fa-chalkboard-teacher", "link": "#"},  # Chalkboard for training and awareness
        {"name": "Continuous Monitoring", "icon": "fas fa-eye", "link": "#"},  # Eye for continuous monitoring
        {"name": "Compliance and Certification", "icon": "fas fa-certificate", "link": "#"},  # Certificate for compliance and certification
        {"name": "Document Management", "icon": "fas fa-folder-open", "link": "#"},  # Folder open for document management
    ]
    context = {
        'page_title': "ISM Dashboard",
        'components': components,
    }
    return render(request, 'ism/dashboard.html', context)

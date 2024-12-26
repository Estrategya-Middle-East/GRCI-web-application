from django.shortcuts import render

# Create your views here.
# CM Dashboard View
def dashboard(request):
    components = [
        {"name": "Governance and Leadership", "icon": "fas fa-users-cog", "link": "#"},  # Users cog for governance and leadership
        {"name": "Risk Assessment and Management", "icon": "fas fa-clipboard-list", "link": "#"},  # Clipboard list for risk assessment
        {"name": "Requirements Management", "icon": "fas fa-clipboard-check", "link": "#"},  # Clipboard check for requirements management
        {"name": "Implementation and Controls", "icon": "fas fa-cogs", "link": "#"},  # Cogs for implementation and controls
        {"name": "Incident Management", "icon": "fas fa-exclamation-triangle", "link": "#"},  # Exclamation triangle for incidents
        {"name": "Monitoring and Auditing", "icon": "fas fa-search", "link": "#"},  # Magnifying glass for monitoring and auditing
        {"name": "Training and Awareness", "icon": "fas fa-chalkboard-teacher", "link": "#"},  # Chalkboard for training
        {"name": "Continuous Improvement", "icon": "fas fa-arrow-circle-up", "link": "#"},  # Arrow up for improvement
        {"name": "Reporting and Communication", "icon": "fas fa-comments", "link": "#"},  # Comments for communication
        {"name": "Documentation Management", "icon": "fas fa-folder-open", "link": "#"},  # Folder open for document management
    ]
    context = {
        'page_title': "CM Dashboard",
        'components': components,
    }
    return render(request, 'cm/dashboard.html', context)

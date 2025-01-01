from django.shortcuts import render

# Create your views here.
# BPM Dashboard View
def dashboard(request):
    components = [
        {"name": "Agenda Setting", "icon": "fas fa-calendar-alt", "link": "#"},  # Calendar for agenda setting
        {"name": "Creation", "icon": "fas fa-pencil-alt", "link": "#"},  # Pencil for creation
        {"name": "Approval", "icon": "fas fa-thumbs-up", "link": "#"},  # Thumbs-up for approval
        {"name": "Implementation", "icon": "fas fa-play-circle", "link": "#"},  # Play circle for implementation
        {"name": "Reporting and Monitoring", "icon": "fas fa-sync-alt", "link": "#"},  # Sync-alt for reporting and monitoring
        {"name": "Maintenance", "icon": "fas fa-wrench", "link": "#"},  # Wrench for maintenance
        {"name": "Dashboard and Monitoring", "icon": "fas fa-tachometer-alt", "link": "#"},  # Tachometer-alt for dashboard and monitoring
    ]
    context = {
        'page_title': "BPM Dashboard",
        'components': components,
    }
    return render(request, 'bpm/dashboard.html', context)

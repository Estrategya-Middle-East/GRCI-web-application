from .hod_views import MODULES  # Import your MODULES list

def visible_modules(request):
    """
    Context processor to make visible modules available globally.
    """
    return {
        'visible_modules': [module for module in MODULES if module["visible"]],
    }
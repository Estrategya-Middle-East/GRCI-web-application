from django import template

register = template.Library()

@register.filter
def get_permission_id(perms, action):
    """
    Fetch the permission ID for a specific action (add, change, delete, view).
    """
    for perm in perms:
        if action in perm.codename:
            return perm.id
    return None
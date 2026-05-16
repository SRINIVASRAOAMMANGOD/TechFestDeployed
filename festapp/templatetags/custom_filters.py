from django import template

register = template.Library()

@register.filter
def can_edit(user):
    """Check if user can perform CRUD operations"""
    return user.is_superuser or user.is_staff or user.groups.filter(name='GeneralUsers').exists()

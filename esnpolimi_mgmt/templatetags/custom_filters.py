from django import template

register = template.Library()


@register.filter
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]


@register.filter
def has_perm(user, permission):
    return user.has_perm(permission)

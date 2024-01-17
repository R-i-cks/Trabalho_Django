from django import template

register = template.Library()

@register.filter(name='is_enfermeiro')
def is_enfermeiro(user):
    return user.groups.filter(name='Enfermeiro').exists()

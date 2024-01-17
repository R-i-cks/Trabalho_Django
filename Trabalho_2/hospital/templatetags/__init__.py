from django import template

register = template.Library()

from . import custom_tags

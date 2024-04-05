from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='mark_required')
def mark_required(field):
    if field.field.required:
        field.label_suffix = " *"  # Append asterisk to label if field is required
    return field

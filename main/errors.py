from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorDict

def nice_errors(form):
    nice_errors = ErrorDict()
    for field, errors in form.errors.items():
        if field == NON_FIELD_ERRORS:
            key = None
        else:
            key = form.fields[field].label
        nice_errors[key] = errors
    return nice_errors
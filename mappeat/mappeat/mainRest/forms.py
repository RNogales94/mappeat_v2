 
from djng.forms import NgFormValidationMixin, NgModelFormMixin
from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class TableForm(NgModelFormMixin, forms.ModelForm):
    """
    Table Form with a little crispy forms added! 
    """
    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        setup_bootstrap_helpers(self)

    class Meta:
        model = Table
        fields = ('number', 'type_table',)

def setup_bootstrap_helpers(object):
    object.helper = FormHelper()
    object.helper.form_class = 'form-horizontal'
    object.helper.label_class = 'col-lg-3'
    object.helper.field_class = 'col-lg-8'
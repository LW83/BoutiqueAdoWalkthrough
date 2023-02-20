from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _  # Used for translation. Using 'as -' means can now call gettext_lazy() using _(). Effectively acts as an alias!


class CustomClearableFileInput(ClearableFileInput): # Inheriting from original class
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)  #Replace image field on form with new one

    def __init__(self, *args, **kwargs):  # Overriding init method 
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()  # get all the categories
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'  # iterating through and setting classes for styling purposes

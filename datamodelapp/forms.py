from django.forms import ModelForm
from .models import DataModel

class DataModelForm(ModelForm):
    class Meta:
        model = DataModel
        fields = '__all__'
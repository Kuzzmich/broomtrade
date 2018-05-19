from goods.models import Good
from goods.models import GoodImage
from django.forms import ModelForm


class GoodForm(ModelForm):
    class Meta:
        model = Good
        fields = '__all__'


class GoodImageForm(ModelForm):
    class Meta:
        model = GoodImage
        fields = '__all__'

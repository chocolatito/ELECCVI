from django.forms import (ModelForm,
                          DateInput, TimeInput,
                          ValidationError)
from .models import Elector, Padron
# from .utils import get_queryset_ElectorForm


# Elector
class ElectorEditForm(ModelForm):

    class Meta:
        model = Elector
        fields = ('dni', 'names', 'surnames')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'


class ElectorCreateForm(ModelForm):
    # user = ModelChoiceField(queryset=get_queryset_ElectorForm())

    class Meta:
        model = Elector
        fields = ('dni', 'names', 'surnames')
        # fields = ('dni', 'names', 'surnames', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'


# Padron
class PadronForm(ModelForm):

    class Meta:
        model = Padron
        fields = ['title', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

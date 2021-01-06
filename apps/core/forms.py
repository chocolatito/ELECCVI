from django.forms import ModelForm, DateInput, TimeInput, ModelChoiceField, HiddenInput
from .models import Elector, Cargo, Eleccion, Candidato, Padron
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


# Cargo
class CargoForm(ModelForm):

    class Meta:
        model = Cargo
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'


# Eleccion
class DateInput(DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class TimeInput(TimeInput):
    input_type = "time"


class EleccionForm(ModelForm):

    class Meta:
        model = Eleccion
        fields = ['title', 'date', 'start_time', 'end_time',
                  'eleccion_padron', 'eleccion_cargo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = DateInput()
        self.fields["start_time"].widget = TimeInput()
        self.fields["end_time"].widget = TimeInput()
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'


# Candidato
class CandidatoForm(ModelForm):

    class Meta:
        model = Candidato
        fields = ('candidato_cargo', 'candidato_elector', 'candidato_eleccion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

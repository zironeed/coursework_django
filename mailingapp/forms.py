from django import forms
from mailingapp.models import MailingSettings, Statistic, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_published":
                field.widget.attrs["class"] = "form-control"


class MailingSettingsCreateForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].empty_label = "Select Message"

    class Meta:
        model = MailingSettings
        fields = ["title", "time", "frequency", "message", "client"]


class ClientCreateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]


class MessageCreateForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ["title", "body"]


class StatisticForm(forms.ModelForm):

    class Meta:
        model = Statistic
        fields = ["status", "answer"]
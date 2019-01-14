from django import forms

from models import ResumeItem, Resume


class ResumeItemForm(forms.ModelForm):
    """
    A form for creating and editing resume items. Note that 'user' is not
    included: it is always set to the requesting user.
    """
    class Meta:
        model = ResumeItem
        fields = ['title', 'company', 'start_date', 'end_date', 'description']


class ResumeForm(forms.ModelForm):
    """
    A form for creating and editing resumes. Note that 'user' is not
    included: it is always set to the requesting user.
    """

    class Meta:
        model = Resume
        fields = ['title', 'resume_items']

    def __init__(self, user, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['resume_items'] = forms.ModelMultipleChoiceField(
            queryset=ResumeItem.objects.filter(user=user),
            required=False,
            help_text='Hold down "Control", or "Command" on a Mac, to select more than one.'
        )

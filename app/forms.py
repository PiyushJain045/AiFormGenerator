from django import forms

class FormGenerationInputForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Form Description",
        help_text="A long, descriptive text explaining the overall purpose of the form."
    )
    objective = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Goal/Objective",
        help_text="A clear, specific goal statement to guide question framing."
    )
    audience = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Target Audience",
        help_text="Context about the respondents (e.g., demographics, roles, experience levels)."
    )
    tone = forms.ChoiceField(
        choices=[('formal', 'Formal'), ('casual', 'Casual'), ('empathetic', 'Empathetic'), ('engaging', 'Engaging')],
        label="Preferred Tone",
        help_text="Specify the desired tone for the form (e.g., formal, casual, empathetic)."
    )
    num_questions = forms.ChoiceField(
        choices=[(1, '1-8'), (2, '9-16'), (3, '17-24'), (4, '24+')],
        label="Number of Questions",
        help_text="Select the range of questions you'd like in the form."
    )
    preferences = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Question Preferences",
        help_text="Provide options for question types (e.g., multiple-choice, Likert scale, open-ended)."
    )
    additional_context = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Additional Context (Optional)",
        required=False,
        help_text="Provide specific questions to include, exclusions, or any special instructions."
    )

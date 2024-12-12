from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import DateInput, TextInput
from django.core.exceptions import ValidationError

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class UserForm(CustomUserForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = User
        fields = CustomUserForm.Meta.fields + ['department']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class DepartmentForm(FormSettings):
    staff = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.filter(department__isnull=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ['name', 'description', 'staff']

class SectionForm(FormSettings):
    staff = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            department = kwargs['instance'].department
            self.fields['staff'].queryset = Staff.objects.filter(department=department, section__isnull=True)

    class Meta:
        model = Section
        fields = ['name', 'description', 'department', 'staff']

class GroupForm(FormSettings):
    staff = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            section = kwargs['instance'].section
            self.fields['staff'].queryset = Staff.objects.filter(section=section, group__isnull=True)

    class Meta:
        model = Group
        fields = ['name', 'description', 'section', 'staff']

class StaffForm(CustomUserForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            instance = kwargs['instance']
            # Filter sections by selected department
            self.fields['section'].queryset = Section.objects.filter(department=instance.department)
            # Filter groups by selected section
            self.fields['group'].queryset = Group.objects.filter(section=instance.section)

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        section = cleaned_data.get('section')
        group = cleaned_data.get('group')

        if group and group.section != section:
            self.add_error('group', "Selected group does not belong to the selected section.")
        if section and section.department != department:
            self.add_error('section', "Selected section does not belong to the selected department.")
        return cleaned_data

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['department', 'section', 'group']


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class UserEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = User
        fields = UserForm.Meta.fields 


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = StaffForm.Meta.fields


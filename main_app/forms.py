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

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        if 'org_chart_level' in self.initial or 'org_chart_level' in self.data:
            # Get the current org_chart_level from initial data or the form's submitted data
            current_level = self.initial.get('org_chart_level', self.data.get('org_chart_level'))

            # Define the hierarchy and determine the parent level
            level_hierarchy = ['N1', 'N2', 'N3', 'N4']
            if current_level in level_hierarchy:
                # Determine the parent level based on the current level
                current_index = level_hierarchy.index(current_level)
                if current_index > 0:  # Ensure there's a parent level to select
                    parent_level = level_hierarchy[current_index - 1]
                    # Filter departments that match the parent level
                    self.fields['parent'].queryset = Department.objects.filter(org_chart_level=parent_level)
                else:
                    self.fields['parent'].queryset = Department.objects.none()  # No parent for N1
            else:
                self.fields['parent'].queryset = Department.objects.none()
        else:
            self.fields['parent'].queryset = Department.objects.none()

    class Meta:
        model = Department
        fields = ['name', 'description', 'org_chart_level', 'parent', 'purpose', 'primary_responsibilities', "key_interfaces", "Key_external_relationships", "key_customer_relationships", "major_systems_and_data_used", "key_suppliers"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'primary_responsibilities': forms.Textarea(attrs={'rows': 3}),
            'key_interfaces': forms.Textarea(attrs={'rows': 3}),
            'Key_external_relationships': forms.Textarea(attrs={'rows': 3}),
            'key_customer_relationships': forms.Textarea(attrs={'rows': 3}),
            'major_systems_and_data_used': forms.Textarea(attrs={'rows': 3}),
            'key_suppliers': forms.Textarea(attrs={'rows': 3}),
        }


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

class StaffForm(CustomUserForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )
    """ section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False
    ) """

    """ def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            instance = kwargs['instance']
            # Filter sections by selected department
            self.fields['section'].queryset = Section.objects.filter(department=instance.department)
            # Filter groups by selected section
            self.fields['group'].queryset = Group.objects.filter(section=instance.section)
 """
    def clean(self):
        cleaned_data = super().clean()
        """ department = cleaned_data.get('department')
        section = cleaned_data.get('section')
        group = cleaned_data.get('group')

        if group and group.section != section:
            self.add_error('group', "Selected group does not belong to the selected section.")
        if section and section.department != department:
            self.add_error('section', "Selected section does not belong to the selected department.") """
        return cleaned_data

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['department']



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


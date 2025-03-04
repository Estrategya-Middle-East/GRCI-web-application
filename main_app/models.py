from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"] is True, "Superuser must have is_staff=True."
        assert extra_fields["is_superuser"] is True, "Superuser must have is_superuser=True."
        return self._create_user(email, password, **extra_fields)





class CustomUser(AbstractUser):
    USER_TYPE = ((1, "1"), (2, "2"), (3, "3")) # ((1, "HOD"), (2, "Staff"), (3, "User"))
    GENDER = [("M", "Male"), ("F", "Female")]

    username = None  # Remove username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=2)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/')
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Adding related_name attributes to avoid conflicts with Django's auth.User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    org_chart_level = models.CharField(
        max_length=50,
        choices=[
            ('N1', 'N1'),
            ('N2', 'N2'),
            ('N3', 'N3'),
            ('N4', 'N4'),
        ],
        default=None,
        null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text='Select the parent department with a higher org_chart_level.'
    )
    introduction_section = models.TextField(null=True, blank=True)
    primary_responsibilities_section = models.TextField(null=True, blank=True)
    team_section = models.TextField(null=True, blank=True)
    governance_section  = models.TextField(null=True, blank=True)
    policies_section = models.TextField(null=True, blank=True)
    challenges_section = models.TextField(null=True, blank=True)
    performance_section = models.TextField(null=True, blank=True)
    technology_section = models.TextField(null=True, blank=True)
    interaction_section = models.TextField(null=True, blank=True)
    regulations_section = models.TextField(null=True, blank=True)
    plans_section = models.TextField(null=True, blank=True)
    raci_matrix_section = models.TextField(null=True, blank=True)
    authority_delegation_section = models.TextField(null=True, blank=True)
    mis_section = models.TextField(null=True, blank=True)
    departmental_swot_section = models.TextField(null=True, blank=True)
    annual_budget_section = models.TextField(null=True, blank=True)
    other_information_section = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Department: {self.department.name})"


class Staff(models.Model):
    ROLE_TYPE = (("Data Entry", "Data Entry"), ("Reviewer", "Reviewer"), ("Approver", "Approver"))
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    role = models.CharField(max_length=50, choices=ROLE_TYPE, blank=True, null=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

    def save(self, *args, **kwargs):
        # Ensure the hierarchy is consistent
        if self.section and self.section.department != self.department:
            raise ValueError("The section does not belong to the selected department.")

        # Assign the department if the section is assigned
        if self.section and not self.department:
            self.department = self.section.department


        super().save(*args, **kwargs)


class User(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"{self.admin.first_name}, {self.admin.last_name}"
    
class Notificationadmin(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Action(models.Model):
    ACTION_TYPE = (
        ("Submit", "Submit"),
        ("Review", "Review"),
        ("Approve", "Approve"),
        ("Reject", "Reject")
        )
    type = models.CharField (max_length=50, choices=ACTION_TYPE, null=True, blank=True)
    owner = models.ForeignKey (Staff, on_delete=models.DO_NOTHING, null=True, blank=True)
    comment = models.TextField (null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.owner} {self.type}"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            User.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.user.save()
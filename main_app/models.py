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


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return f"From {self.start_year} to {self.end_year}"


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "User"))
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
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

    def save(self, *args, **kwargs):
        # Ensure the hierarchy is consistent
        if self.group and self.group.section != self.section:
            raise ValueError("The group does not belong to the selected section.")
        if self.section and self.section.department != self.department:
            raise ValueError("The section does not belong to the selected department.")

        # Assign the department if the section is assigned
        if self.section and not self.department:
            self.department = self.section.department

        # Assign the section if the group is assigned
        if self.group and not self.section:
            self.section = self.group.section

        super().save(*args, **kwargs)


class User(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

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
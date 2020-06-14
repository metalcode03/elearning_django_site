from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from classes.models import Class, Subject, Lesson

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if not email:
            ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        user.active = True

        user.set_password(password)
        user.save(using=self._db)

        return user

    # HANDLING SUPERUSER MANAGEMENT WHICH IS THE ADMIN

    def create_superuser(self, username, email, password=None):

        user = self.create_user(
            username,
            email,
            password=password
        )

        user.admin = True
        user.staff = True
        user.active = True
        user.teacher = True
        user.student = True

        user.save(using=self._db)

        return user

    # HANDLING STAFF USER MANAGEMENT

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password
        )

        user.staff = True
        user.active = True
        user.teacher = True
        user.student = True

        user.save(using=self._db)

        return user

    # HANDLING BUS USER MANAGEMENT

    def create_teacher(self, username, email, password=None):

        user = self.create_user(
            username,
            email,
            password=password
        )

        user.active = True
        user.teacher = True
        user.student = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=300,
        unique=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alphanumeric or contain number',
                code='invalid_username',
            )
        ]
    )
    email = models.EmailField(
        max_length=300,
        unique=True,
        verbose_name='email address',
    )
    
    active = models.BooleanField(default=True)
    admin= models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    student = models.BooleanField(default=True)
    teacher = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.email
    def get_long_name(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active
    @property
    def is_student(self):
        return self.student
    @property
    def is_teacher(self):
        return self.teacher


class Profile(models.Model):
    SEXCHOICE = (
        ('MA', _('Male')),
        ('FA', _('Female')),
        ('OT', _('Others')),
    )
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to='profile_img', default='avatar.jpg', blank=True)
    sex = models.CharField(
        max_length=253,
        choices=SEXCHOICE,
        default=SEXCHOICE[2],
        blank=True,
    )
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user.username
    


@receiver(post_save, sender=User)
def _post_save_receiver(instance, created, sender, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        
@receiver(post_save, sender=User)
def profile_post_saver(sender, instance, **kwargs):
    instance.profile.save()
    
    
class Student(models.Model):
    student = models.OneToOneField("Profile", on_delete=models.CASCADE)
    # school = models.ManyToManyField("School", blank=True,)
    
    class Meta:
        verbose_name = 'Students'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student.user.username


class School(models.Model):
    schoolUser = models.OneToOneField("Profile", on_delete=models.CASCADE)
    schoolName = models.CharField(max_length=255)
    schoolLogo = models.ImageField(upload_to='School_logo', blank=True)
    backgroundPicture = models.ImageField(upload_to=True, blank=True)
    classes = models.ForeignKey(Class, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Schools'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.schoolName
    

class Teacher(models.Model):
    teacher = models.OneToOneField("Profile", on_delete=models.CASCADE)
    school = models.OneToOneField("School", on_delete=models.DO_NOTHING, blank=True)
    
    def __str__(self):
        return self.teacher.user.username
    
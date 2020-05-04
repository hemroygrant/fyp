from django.db import models
from django.conf import settings
from django.utils import timezone
import PIL
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.

class PasswordUser(models.Model):
    A = 'Alphanumeric'
    O = 'Old Passpoints'
    N = 'New Passpoints'
    PW_SCHEMES =[
        (A, 'Alphanumeric'),
        (O, 'Old Passpoints'),
        (N, 'New Passpoints'),
    ]
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'M'),
        (FEMALE, 'F'),
    ]
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=2, choices=GENDERS)
    age = models.IntegerField()
    pw_user = models.BooleanField()
    remember_pw = models.BooleanField()
    pw_scheme = models.CharField(max_length=14, choices=PW_SCHEMES)
    date_registered = models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s'%(self.first_name, self.last_name, self.email, self.gender, self.age, self.pw_scheme, self.date_registered)

class TextInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s %s'%(self.uid, self.email, self.password)

class OldPpInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    cp_id = models.ForeignKey('ClickPoint', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s'%(self.uid, self.cp_id)

class NewPpInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    cp_id = models.ForeignKey('ClickPoint', on_delete=models.CASCADE)
    img_number = models.SmallIntegerField()

    def __str__(self):
        return '%s %s'%(self.uid, self.cp_id)

class CreateInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    time_create = models.TimeField()

    def __str__(self):
        return '%s %s %s'%(self.uid, self.date_created, self.time_create)

class ConfirmInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    date_confirmed = models.DateTimeField(default=timezone.now)
    time_confirm = models.TimeField()

    def __str__(self):
        return '%s %s %s'%(self.uid, self.date_confirmed, self.time_confirm)

class SubmitInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(default=timezone.now)
    time_submit = models.TimeField()

    def __str__(self):
        return '%s %s %s'%(self.uid, self.date_submitted, self.time_submit)

class LoginInfo(models.Model):
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    date_login = models.DateTimeField(default=timezone.now)
    time_login = models.TimeField()
    login_period = models.SmallIntegerField()

    def __str__(self):
        return '%s %s %s %s'%(self.uid, self.date_login, self.time_login, self.login_period)

class SusResult(models.Model):
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    ANSWER =[
        (one, '1'),
        (two, '2'),
        (three, '3'),
        (four, '4'),
        (five, '5'),
    ]
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    date_answered = models.DateTimeField(default=timezone.now)
    q1 = models.SmallIntegerField(choices=ANSWER)
    q2 = models.SmallIntegerField(choices=ANSWER)
    q3 = models.SmallIntegerField(choices=ANSWER)
    q4 = models.SmallIntegerField(choices=ANSWER)
    q5 = models.SmallIntegerField(choices=ANSWER)
    q6 = models.SmallIntegerField(choices=ANSWER)
    q7 = models.SmallIntegerField(choices=ANSWER)
    q8 = models.SmallIntegerField(choices=ANSWER)
    q9 = models.SmallIntegerField(choices=ANSWER)
    q10 = models.SmallIntegerField(choices=ANSWER)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s'%(self.uid, self.date_answered, self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8, self.q9, self.q10)

class Image(models.Model):
    USER_IMAGE = 'User Image'
    NATURE = 'Nature'
    FOOD = 'Food'
    ANIMAL = 'Animal'
    SPORTS = 'Sports'
    CARS = 'Cars'
    ART = 'Art'

    CATEGORIES =[
        (USER_IMAGE, 'User Image'),
        (NATURE, 'Nature'),
        (FOOD, 'Food'),
        (ANIMAL, 'Animal'),
        (SPORTS, 'Sports'),
        (CARS, 'Cars'),
        (ART, 'Art'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORIES)
    image = models.ImageField(upload_to="password_images/")
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s %s'%(self.image, self.category, self.date_added)

class ClickPoint(models.Model):
    iid = models.ForeignKey('Image', on_delete=models.CASCADE)
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    x_location = models.SmallIntegerField()
    y_location = models.SmallIntegerField()
    color = models.CharField(max_length=250)
    order = models.SmallIntegerField()
    img_number = models.SmallIntegerField()

    def __str__(self):
        return '%s %s %s %s %s %s'%(self.uid, self.iid, self.x_location, self.y_location, self.color, self.order)

class ClickPointFail(models.Model):
    iid = models.ForeignKey('Image', on_delete=models.CASCADE)
    uid = models.ForeignKey('PasswordUser', on_delete=models.CASCADE)
    x_location = models.SmallIntegerField()
    y_location = models.SmallIntegerField()
    color = models.CharField(max_length=250)
    order = models.SmallIntegerField()
    img_number = models.SmallIntegerField()
    date_fail = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s %s %s %s %s %s'%(self.uid, self.iid, self.x_location, self.y_location, self.color, self.order, self.date_fail)
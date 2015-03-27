import hashlib

from django.db import models



# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class User(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=40)
    courses = models.ManyToManyField(Course, through='UserCourses')

    # 0 for student / 1 for admin
    role = models.IntegerField()

    def is_admin(self):
        return self.role == 1


class UserCourses(models.Model):
    subscriptionDate = models.DateTimeField()
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)


class Laboratory(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    course = models.ForeignKey(Course)
    insertionDate = models.DateTimeField()
    openDate = models.DateTimeField()
    closeDate = models.DateTimeField()
    replaceMain = models.BooleanField(True)
    mainReplacement = models.TextField()
    inputStream = models.TextField()
    expectedOutput = models.TextField()


class LaboratoryFile(models.Model):
    title = models.CharField(max_length=30, null=True)
    file = models.FilePathField()
    laboratory = models.ForeignKey(Laboratory)

    def hash(self):
        h = hashlib.md5(str(self.id))
        return h.hexdigest()


class LaboratorySubmission(models.Model):
    dateSubmitted = models.DateTimeField()
    zippedFile = models.FilePathField()
    status = models.CharField(max_length=25)
    grade = models.FloatField(null=True)
    user = models.ForeignKey(User)
    laboratory = models.ForeignKey(Laboratory)


class SubmittedFile(models.Model):
    laboratorySubmission = models.ForeignKey(LaboratorySubmission)
    file = models.FilePathField()


class CorrectionErrors(models.Model):
    laboratorySubmission = models.ForeignKey(LaboratorySubmission)
    type = models.CharField(max_length=12)
    description = models.TextField()


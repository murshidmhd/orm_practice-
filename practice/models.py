from django.db import models


class ActiveStudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Department(models.Model):
    department = models.CharField(max_length=200)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    marks = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)

    active = ActiveStudentManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "student_table"


class Profile(models.Model):
    name = models.OneToOneField(Student, on_delete=models.CASCADE)
    age = models.IntegerField()


class Person(models.Model):
    name = models.CharField(max_length=100)


class Child(Person):
    student_id = models.CharField(max_length=20)


class Teacher(Person):
    salary = models.DecimalField(max_digits=10, decimal_places=2)




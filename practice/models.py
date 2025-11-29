from django.db import models


class TopStudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(marks__gte=80)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    marks = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-marks"]

    def __str__(self):
        return f"{self.name} - {self.marks}"


class TopStudent(Student):
    objects = TopStudentManager()

    class Meta:
        proxy = True
        ordering = ["marks"]


class AuditModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Product(AuditModel):
    name = models.CharField(max_length=100, default="Unnamed")
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "store_product"

    def __str__(self):
        return f"{self.name} - {self.price}"


class Category(AuditModel):
    pass

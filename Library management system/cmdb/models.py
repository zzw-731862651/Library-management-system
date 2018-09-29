from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=32,unique=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    pub_date = models.DateField()
    publish = models.ForeignKey(to='Publish',to_field='id',on_delete=models.CASCADE)
    authors = models.ManyToManyField(to='Author')

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)

    def  __str__(self):
        return self.title

class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    ad = models.OneToOneField(to='AuthorDetail',to_field='id',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AuthorDetail(models.Model):
    gf = models.CharField(max_length=32)
    tel = models.CharField(max_length=32)


class Emp(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=8,decimal_places=2)
    dep = models.CharField(max_length=32)
    province = models.CharField(max_length=32)

class User(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)










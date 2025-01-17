from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class FoodItem(models.Model):
    food_name=models.CharField(max_length=50)
    price=models.IntegerField()
    img=models.ImageField(upload_to="food_img/")
    


class AddtoBag(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    food_item=models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.IntegerField(default=0)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(max_length=50)


STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('packed','Packed'),
    ('One_the_way','On The WAY'),
    ('Delivered','Delivered'),
)

class PlaceOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    food_item=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(choices=STATUS_CHOICE,max_length=50,default="Pending")
    
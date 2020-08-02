from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.


Category = (
    (1, 'Payloop'),
    (2, 'Education')
)


class Product(models.Model):
    category = models.IntegerField(choices=Category, default=1)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    icon = models.ImageField(upload_to='product_icons')
    content = RichTextField()
    video = models.CharField(max_length=20)
    gallery1 = models.ImageField(upload_to='gallery_images')
    gallery2 = models.ImageField(upload_to='gallery_images', blank=True, null=True)
    gallery3 = models.ImageField(upload_to='gallery_images', blank=True, null=True)
    gallery4 = models.ImageField(upload_to='gallery_images', blank=True, null=True)

    class Meta:

        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def __str__(self):

        return self.name


class Packages(models.Model):
    PackageType = (
        (1, 'All Package'),
        (2, 'Custom'),
        (3, 'Single Package'),
    )

    name = models.CharField(max_length=10)
    p_type = models.IntegerField(choices=PackageType)
    des = models.TextField()

    class Meta:
        verbose_name_plural = 'Packages'
        verbose_name = 'Packages'

    def __str__(self):

        return self.name


class ClientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    address = models.TextField()
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    modules = models.CharField(max_length=50, blank=True, null=True)
    reg_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Clients Profile'
        verbose_name = 'Client Profile'

    def __str__(self):

        return self.user.get_full_name()


class BannerText(models.Model):
    title = models.CharField(max_length=254)
    highlight = models.CharField(max_length=254)
    content = models.TextField()
    activate = models.BooleanField()


class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField()


class DemoList(models.Model):
    DemoType = (
        ('education', 'Education Modules'),
        ('ERP', 'Enterprise Resource Planning'),

    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    company_name = models.CharField(max_length=50)
    company_address = models.TextField()
    demo_type = models.CharField(choices=DemoType, max_length=10)


class Education(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    icon = models.ImageField(upload_to='product_icons')
    content = RichTextField()
    video = models.CharField(max_length=20)
    gallery1 = models.ImageField(upload_to='gallery_images', blank=True, null=True)
    gallery2 = models.ImageField(upload_to='gallery_images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Education Products'
        verbose_name = 'Education Product'

    def __str__(self):
        return self.name


class ClientModule(models.Model):
    MODULE_TYPE = (
        ('erp', 'ERP'),
        ('education', 'Education')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    education = models.ForeignKey(Education, on_delete=models.CASCADE, null=True)
    module_type = models.CharField(choices=MODULE_TYPE, default=MODULE_TYPE[0][0], max_length=12)
    last_pay_date = models.DateField(null=True, blank=True)
    next_pay_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    suspend = models.BooleanField(default=False)


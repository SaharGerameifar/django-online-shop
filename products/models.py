from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_filter', args=[self.slug,])


class ProductImageGallery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField()
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    category = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField()
    image_gallery = models.ManyToManyField(ProductImageGallery, blank=True)
    description = RichTextField()
    price = models.IntegerField()
    has_discount = models.BooleanField(default=False)
    super_price = models.IntegerField(default=0, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    related_product = models.ManyToManyField('self', blank=True)
    tag = models.ManyToManyField(Tag, blank=True, related_name='tag_products')
    rates = GenericRelation(Rating)
    hits = models.ManyToManyField(IPAddress, through='ProductHit', blank=True, related_name='hits')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug,])

    def get_superprice_percent(self):
        percent = (self.price - self.super_price) / self.price * 100 
        return int(percent)

    def user_can_like(self, user):
        user_like = user.userlikes.filter(product=self)
        if user_like.exists():
            return True
        return False

    def user_can_save(self, user):
        user_save = user.usersaves.filter(product=self)
        if user_save.exists():
            return True
        return False    

    def comments_count(self):
            return self.productcomments.filter(is_active=True).count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productcomments')
    description = RichTextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replycomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.description[:30]}'

    def get_active_replies_comment(self):
        return self.replycomments.filter(is_active=True)       


class Slider(models.Model):
    name = models.CharField(max_length=150)
    link = models.URLField(max_length=100)
    description = RichTextField()
    image = models.ImageField()

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlikes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productlikes')

    def __str__(self):
        return f'{self.user.full_name} like {self.product.slug}'


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usersaves')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productsaves')

    def __str__(self):
        return f'{self.user.full_name} like {self.product.slug}'


class ProductHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

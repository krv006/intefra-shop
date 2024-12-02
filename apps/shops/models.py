from django.db.models import Model, PositiveIntegerField, ForeignKey, CASCADE, EmailField, ImageField, TextChoices, \
    SmallIntegerField, BooleanField, URLField, TextField, CharField, DateTimeField, Model, SlugField, DateField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class TimeBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.created_at} - {self.updated_at}'


class Category(MPTTModel, BaseSlugModel):
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    background_image = ImageField(upload_to='categories/')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"{self.name}"


class Product(Model):
    class Size(TextChoices):
        F50 = '50', '50'
        F52 = '52', '52'
        F54 = '54', '54'
        F56 = '56', '56'

    class Poll(TextChoices):
        MALE = 'Male', 'male'
        FEMALE = 'Female', 'female'

    class Color(TextChoices):
        WHITE = 'White', 'white'
        RED = 'Red', 'red'
        BLUE = 'Blue', 'blue'
        GREEN = 'Green', 'green'
        YELLOW = 'Yellow', 'yellow'
        BROWN = 'Brown', 'brown'
        GREY = 'Grey', 'grey'
        SKY_BLUE = 'Sky Blue', 'sky blue'
        BLACK = 'Black', 'black'

    name = CharField(max_length=255)
    price = PositiveIntegerField(db_default=0)
    description = CKEditor5Field()
    discount_price = SmallIntegerField(db_default=0, null=True, blank=True)
    size = CharField(max_length=2, choices=Size.choices, db_default=Size.F50)
    poll = CharField(max_length=10, choices=Poll.choices, db_default=Poll.MALE)
    color = CharField(max_length=255, choices=Color.choices, db_default=Color.WHITE)
    material = CharField(max_length=255, null=True, blank=True)
    lining = CharField(max_length=255, null=True, blank=True)  # todo podkladka
    made_from = CharField(max_length=255, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)
    category = ForeignKey('shops.Category', CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.price}, {self.category}"

    # TODO discount_price mana shuni kiritganda nechi foiz sale boletganini xam chiqazib berishi kerak -> ustozdan sorimiz
    # TODO sale nechi foiz kiritganda shunda summasini ozi aftamatik olishi kerak -> ustozdan sorimiz


class Address(Model):
    class Type(TextChoices):
        HOME = 'Доставка на дом', 'доставка на дом'
        FILIAL = 'Пункт выдачи СДЭК', 'пункт выдачи СДЭК'
        RUSSIAN = 'Россия', 'pоссия'

    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    city = CharField(max_length=100)
    home_number = CharField(max_length=100)
    deliver_place = CharField(max_length=100, choices=Type.choices, db_default=Type.RUSSIAN)
    email = EmailField()
    phone_number = CharField(max_length=100)
    description = TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"


class Brand(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='brand/')

    def __str__(self):
        return f"{self.name}"


class Payment(Model):
    name = CharField(max_length=255)
    surname = CharField(max_length=255)
    delivery_home = BooleanField(db_default=True)
    SDEK_pickup_point = BooleanField(db_default=False)
    region = CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}, {self.delivery_home}"


class Image(Model):
    image = ImageField(upload_to='images/product/')
    product = ForeignKey('shops.Product', CASCADE, related_name='images')


class Order(TimeBaseModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVERING = "delivering", 'Delivering'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        BROKEN = "broken", 'Broken'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = "archived", 'Archived'

    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW, verbose_name="status")
    product = ForeignKey('shops.Product', CASCADE, related_name='orders')
    address = ForeignKey('shops.Address', CASCADE, related_name='orders')
    owner = ForeignKey('users.User', CASCADE, related_name='orders')
    payment = ForeignKey('shops.Payment', CASCADE, related_name='orders')
    operator = ForeignKey('users.Operator', CASCADE, null=True, blank=True, related_name='orders')
    send_order_date = DateField(null=True, blank=True, verbose_name="send order date")
    comment_operator = CharField(max_length=255, null=True, blank=True,
                                 verbose_name="the operator's comment for the order")

    def __str__(self):
        return self.status

    @property
    def order_count(self):
        return self.status.count('new')


class OrderItem(Model):
    order = ForeignKey('shops.Order', CASCADE, related_name='items')
    product = ForeignKey('shops.Product', CASCADE)
    quantity = PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"


class QuickOrder(Model):
    name = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    order = ForeignKey('shops.Product', CASCADE, related_name='quick_orders')


class SiteSettings(Model):
    instagram = URLField()
    telegram = URLField()

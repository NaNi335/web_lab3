from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================== people ===========================
class User(AbstractUser):
    phone_number = models.CharField("Телефон", max_length=15, blank=True, null=True)
    roles = (
        ('ad', 'Администратор'),
        ('ma', 'Менеджер'),
        ('ac', 'Бухгалтер'),
    )

    role = models.CharField(max_length=20, choices=roles)
    first_name = models.CharField(max_length=100)

    REQUIRED_FIELDS = ['first_name', 'phone_number', 'role']

    def __str__(self):
        return "{}-{}".format(self.username, self.role)


class Executor(models.Model):
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')

    def __str__(self):
        return self.full_name


class Client(models.Model):
    contact_person = models.CharField(max_length=60, verbose_name='Контактное лицо')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    email = models.EmailField(max_length=30, verbose_name='Электронный адрес')
    bank_details = models.CharField(max_length=30, verbose_name='Банковские реквизиты')

    def __str__(self):
        return "{}".format(self.contact_person)


# =========================== products ===========================
class MaterialsPL(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование материала')
    price = models.CharField(max_length=30, verbose_name='Цена')

    def __str__(self):
        return self.title


class ServicesPL(models.Model):
    service_types = (
        ('у', 'уличная реклама'),
        ('и', 'реклама в интерьере внутри помещения'),
        ('т', 'реклама на транспортных средствах'),
        ('п', 'печатная реклама'),
    )

    service_type = models.CharField(max_length=20, choices=service_types, verbose_name='Вид услуги')
    title = models.CharField(max_length=50, verbose_name='Наименование услуги')
    price = models.CharField(max_length=30, verbose_name='Стоимость услуги')

    def __str__(self):
        return self.title


# =========================== orders ===========================
class Request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Заказчик')
    request_date = models.DateField(verbose_name='Дата заявки')
    workload = models.CharField(max_length=30, verbose_name='Объем работ')
    price = models.CharField(max_length=30, verbose_name='Итоговая стоимость')
    statuses = (
        ('н', 'не оплачено'),
        ('о', 'оплачено'),
    )
    status = models.CharField(max_length=20, choices=statuses, verbose_name='Состояние')

    def __str__(self):
        return "{}-{}-{}".format(self.id, self.request_date, self.client.contact_person)


class Invoice(models.Model):
    request = models.ForeignKey(Request, verbose_name='Заявка', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE)
    pay_due = models.DateField(verbose_name='Срок платежа')

    def __str__(self):
        return "{}-{}".format(self.id, self.client.contact_person)


class PaymentOrder(models.Model):
    request = models.ForeignKey(Request, verbose_name='Заявка', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, verbose_name='Счет на оплату', on_delete=models.CASCADE)
    pay_date = models.DateField(verbose_name='Дата оплаты')


# =========================== relationships ===========================
class ChosenServices(models.Model):
    service = models.ForeignKey(ServicesPL, verbose_name='Выбранная услуга', on_delete=models.CASCADE)
    request = models.ForeignKey(Request, verbose_name='Заявка', on_delete=models.CASCADE)
    total_cost = models.CharField(max_length=30, verbose_name='Общая стоимость услуг')


class ChosenMaterials(models.Model):
    material = models.ForeignKey(MaterialsPL, verbose_name='Выбранный материал', on_delete=models.CASCADE)
    request = models.ForeignKey(Request, verbose_name='Заявка', on_delete=models.CASCADE)
    total_cost = models.CharField(max_length=30, verbose_name='Общая стоимость материалов')
    amount = models.IntegerField(verbose_name='Количество материалов(шт.)')


class WorkGroup(models.Model):
    request = models.ForeignKey(Request, verbose_name='Заявка', on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, verbose_name='Исполнитель', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='Дата начала работы')
    end_date = models.DateField(verbose_name='Дата окончания работы')

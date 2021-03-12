# Эндпоинты, связанные с моделью Client

---

### Модель:
_models.py_
```
class Client(models.Model):
    contact_person = models.CharField(max_length=60, verbose_name='Контактное лицо')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    email = models.EmailField(max_length=30, verbose_name='Электронный адрес')
    bank_details = models.CharField(max_length=30, verbose_name='Банковские реквизиты')

    def __str__(self):
        return "{}".format(self.contact_person)
```

### Просмотр всех клиентов(с возможностью фильтрации по _legal_entity_):
_serializer.py_
```
class InvoiceViewNestedSerializer(serializers.ModelSerializer):

    request = RequestWStatusViewSerializer()
    client = ClientViewSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
```

_views.py_
```
class ClientListAPIView(generics.ListAPIView):

    serializer_class = ClientViewSerializer

    def get_queryset(self):
        queryset = Client.objects.all()
        params = self.request.query_params

        legal_entity = params.get('legal_entity', None)

        if legal_entity:
            queryset = queryset.filter(legal_entity=legal_entity)

        return queryset
```

_urls.py_
```
urlpatterns = [
    path('client/', ClientListAPIView.as_view()),
    ...
    ]
```
---

### Создание клиента:
_serializer.py_

```
class ClientCreateSerializer(serializers.Serializer):

    legal_entity = serializers.CharField(max_length=60)
    contact_person = serializers.CharField(max_length=60)
    phone_number = serializers.CharField(max_length=12)
    email = serializers.CharField(max_length=30)
    bank_details = serializers.CharField(max_length=30)

    def create(self, validated_data):
        client = Client(**validated_data)
        client.save()
        return Client(**validated_data)
```

_views.py_
```
class ClientCreateAPIView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer
```

_urls.py_
```
urlpatterns = [
    ...
    path('client/create/', ClientCreateAPIView.as_view()),
    ...
    ]
```
---

### Просмотр/изменение/удаление клиента по id:
_serializer.py_
```
class ClientViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = "__all__"
```
_views.py_
```
class ClientRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientViewSerializer
```
_urls.py_
```
urlpatterns = [
    ...
    path('client/<int:pk>/', ClientRUDAPIView.as_view()),
    ...
    ]
```
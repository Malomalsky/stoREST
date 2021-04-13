# stoREST
storage REST API

---

API можно найти по адресу [malomalsky.studio](http://malomalsky.studio)

Все запросы стоит направлять туда. 

---

## Использование

| Путь        | Метод  | Заголовки                                        | Тело запроса           | Результат                                                                                                                                 |
|-------------|--------|--------------------------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /resources  | GET    | -                                                | -                      | Список всех ресурсов;  Общее количество ресурсов.                                                                                         |
| /resources  | POST   | -                                                | JSON с данными ресурса | 201 - если ресурс создан успешно;  <br/> 409 - если ресурс с таким title уже есть в БД;  <br/> 400 - если внесены неправильные параметры. |
| /resources  | DELETE | Content-Type: application/x-www-form-urlencoded  | id=                    | 204 - если удалено успешно; <br/> 400 - если в запросе синтаксические ошибки;  <br/> 409 - если на сервере нет ресурса с таким id;        |
| /resources  | PUT    | Content-Type: application/x-www-form-urlencoded  | id=id&title=title&amount=amount&unit=unit&price=price&date=date |  200 - если изменение успешно; <br/> 400 - если не передан id; <br/> 422 - если в запросе невалидируемые данные                                                                                                                                         |
| /resources  | PATCH  | Content-Type: application/x-www-form-urlencoded  | id=id(обязательно)&parametr=parametr |    Те же, что и в PUT                                                                                                                                       |
| /total_cost |  GET   |  -                                               | -                      | JSON с суммой цен всех ресурсов                                                                                                                                          |


Все коды ответов соотевтствуют спецификациям RFC. 

## Примеры

### /resources

Создание ресурса: 

```shell
curl --location --request POST 'http://malomalsky.studio/resources/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Доска", 
    "amount": 1000, 
    "unit": "шт.", 
    "price": 15, 
    "date": "2021-04-13"
}'
```

response

```json
{
    "id": 3,
    "title": "Доска",
    "amount": 1000.0,
    "unit": "шт.",
    "price": 15.0,
    "date": "2021-04-13"
}
```

Получение списка всех ресурсов: 

```shell
curl --location --request GET 'http://malomalsky.studio/resources/'
```

response

```json
{
    "resources": [
        {
            "id": 1,
            "title": "Гвоздь",
            "amount": 1000.0,
            "unit": "шт.",
            "price": 12.0,
            "date": "2021-04-13"
        },
        {
            "id": 3,
            "title": "Доска",
            "amount": 1000.0,
            "unit": "шт.",
            "price": 15.0,
            "date": "2021-04-13"
        }
    ],
    "total_count": 2
}
```

Удаление ресурса с id=3

```shell
curl --location --request DELETE 'http://malomalsky.studio/resources/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=3'
```

```shell
204 No Content
```

Изменение цены гвоздей

```shell
curl --location --request PATCH 'http://malomalsky.studio/resources/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=1' \
--data-urlencode 'price=750'
```

```shell
200 OK
```

Полное изменение гвоздей

```shell
curl --location --request PUT 'http://malomalsky.studio/resources/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=1' \
--data-urlencode 'price=800' \
--data-urlencode 'title=Гвоздик' \
--data-urlencode 'amount=15' \
--data-urlencode 'unit=Пачка' \
--data-urlencode 'date=2021-12-04'
```

```shell
200 OK
```

Очень важно включать заголовок **Content-Type: application/x-www-form-urlencoded** в запросы, которые принимает параметры в POST-форме

### /total_cost

Получить цену всех ресурсов на складе

```shell
curl --location --request GET 'http://malomalsky.studio/total_cost/'
```

response

```json
{
    "total_cost": 800.0
}
```


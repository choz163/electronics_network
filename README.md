# electronics_network

Сервис управления иерархической сетью торговых точек и складами с возможностью учёта задолженностей и привязки товаров.

## Описание

Проект предоставляет:

- Модель NetworkNode с иерархией поставщиков (до любого уровня вложенности).
- Модель Product, привязанную к узлу сети.
- Административную панель Django с фильтрацией, поиском и action-обновлениями.
- REST API (Django REST Framework) с CRUD, фильтрацией по стране и правами доступа.
- Блокировку изменения задолженности (debt_to_supplier) через API.

## Технологии

- Python 3.8+
- Django 3.2+
- Django REST Framework
- django-filter
- PostgreSQL 10+
- Git

## Структура проекта


electronics_network/
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── electronics_network/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md



## Установка

1. Клонировать репозиторий:

git clone https://github.com/choz163/electronics_network.git
cd electronics_network



2. Настроить виртуальное окружение:

python3 -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows



3. Установить зависимости:

pip install -r requirements.txt



4. Настроить подключение к базе данных в `electronics_network/settings.py`:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '4815ь',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



Применить миграции:


python manage.py makemigrations
python manage.py migrate



Создать суперпользователя:


python manage.py createsuperuser



Запустить сервер:


python manage.py runserver



Административная панель

URL: http://127.0.0.1:8000/admin/



Модель Узел сети (NetworkNode):

Вывод: name, city, country, поставщик (с ссылкой), debt_to_supplier, created_at.

Фильтрация по городу, поисковые поля: name, city, country.

Action “Обнулить задолженность перед поставщиком”.



Модель Продукт (Product):

Вывод: title, model, node, release_date.

Фильтрация по дате релиза и по имени узла, поиск по title и model.




API

Все эндпоинты доступны по базовому пути /api/. Доступ — только для активных штатных пользователей (is_active ∧ is_staff) через BasicAuth/SessionAuth.


NetworkNode


GET    /api/nodes/

Список узлов. Поддерживается фильтрация: ?country=Russia

POST   /api/nodes/

Создать узел. Пример тела:
{
  "name": "Магазин №1",
  "email": "shop1@example.com",
  "country": "Russia",
  "city": "Moscow",
  "street": "Тверская",
  "house_number": "10",
  "supplier": 1,
  "debt_to_supplier": "500.00"
}
Копировать


GET    /api/nodes/{id}/

Детали узла (включая список products).

PUT    /api/nodes/{id}/

Полное обновление (любое поле, кроме debt_to_supplier будет проигнорировано при обновлении задолженности).

PATCH  /api/nodes/{id}/

Частичное обновление.

DELETE /api/nodes/{id}/

Удаление узла.


Product

CRUD эндпоинты не вынесены отдельно, управляются через админку и nested-сериализацию NetworkNode.


Особенности


Поле level вычисляется динамически и показывает глубину узла в иерархии поставщиков.

Задолженность debt_to_supplier может быть только обнулена массовым action в админке.

В API изменение debt_to_supplier игнорируется.

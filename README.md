# VNE Techwear Store - Backend API
## Backend для интернет-магазина techwear бренда VNE. Реализован на FastAPI с использованием PostgreSQL.

### Функционал
  * Получение списка товаров с фильтрацией

  * Получение детальной информации о товаре

  * Добавление новых товаров

  * Удаление товаров

  * Поиск по названию и категории

  * Валидация данных

### Технологии
* FastAPI 

* PostgreSQL 

* SQLAlchemy 

* Docker 

* Pydantic 


### 1: Запуск через Docker 

#### Клонируйте репозиторий:

* git clone <url-репозитория>
* cd techwear-store
#### Запустите все сервисы:

* docker-compose up -d
#### Приложение будет доступно по адресам:

* API: http://localhost:8000

* Документация Swagger: http://localhost:8000/docs

* Альтернативная документация: http://localhost:8000/redoc

### 2: Локальная установка
#### Убедитесь, что установлен Python 3.11+ и PostgreSQL

#### Создайте виртуальное окружение:

* python -m venv venv
* source venv/bin/activate  # Linux/MacOS
#### или
* venv\Scripts\activate     # Windows
#### Установите зависимости:

* pip install -r requirements.txt

#### Запустите PostgreSQL и создайте базу данных:

    CREATE DATABASE techwear_db;
    CREATE USER techwear_user WITH PASSWORD 'pass';
    GRANT ALL PRIVILEGES ON DATABASE techwear_db TO techwear_user;

#### Запустите приложение:

* cd app
* uvicorn main:app --reload


### API Endpoints
 1. Получить список товаров
     * GET /products

#### Параметры:

* category (опционально) - фильтр по категории

* name (опционально) - поиск по названию

* skip - смещение (по умолчанию 0)

* limit - лимит (по умолчанию 100)

2. Получить информацию о товаре
   * GET /products/{id}

3. Добавить новый товар
   * POST /products


    {
      "name": "Waterproof Jacket",
      "description": "Техническая куртка с мембраной",
      "price": 299.99,
      "category": "jackets",
      "sizes": "S,M,L,XL"
    }

4. Удалить товар
   * DELETE /products/{id}


### Примеры использования
* Получить все товары curl -X 'GET' 'http://localhost:8000/products'
* Поиск товаров по категории  curl -X 'GET' 'http://localhost:8000/products?category=jackets'
* Поиск по названию curl -X 'GET' 'http://localhost:8000/products?name=waterproof'
* Добавить новый товар curl -X 'POST' 'http://localhost:8000/products' \ 
-H 'Content-Type: application/json' \
-d '{
  "name": "Tech Pants",
  "description": "Функциональные штаны с карго",
  "price": 199.99,
  "category": "pants",
  "sizes": "M,L,XL"
}'


### Переменные окружения

 * DATABASE_URL=postgresql://user:password@host:port/database
 * По умолчанию используется:
    
    Хост: localhost
    
    Порт: 5432
    
    База данных: techwear_db
    
    Пользователь: techwear_user
    
    Пароль: pass




### Тестирование

    pytest tests/
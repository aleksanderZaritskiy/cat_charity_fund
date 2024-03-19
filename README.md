# fastapi project - CAT_CHARITY_FUND

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-0.70.0-green?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.23-blue?style=for-the-badge&logo=sqlalchemy&logoColor=white)

## Использованные при реализации проекта технологии
 - Python
 - fastapi
 - SQLAlchemy

## Установка проекта на локальный компьютер из репозитория 

### Для установки проекта необходимо выполнить следующие шаги:

### Базовая настройка:
 - Клонировать репозиторий `git clone git@github.com:aleksanderZaritskiy/cat_charity_fund.git`
 - Перейти в директорию с клонированным репозиторием
 - установить и развернуть виртуальное окружение
 - обновить pip и установить зависимости
 - выполнить команду по созданию миграций alembic revision --autogenerate -m 'y. comment'
 - выполнить команду для выполнения миграций alembic upgrade head
 - для автоматического создания суперюзера при запуске проекта создайте в файле с переменными окружения .env FIRST_SUPERUSER_EMAIL и FIRST_SUPERUSER_PASSWORD
 - подключить переменные к core.config.Settings
 - запустить проект app.main:app

---

### Инструкция по API:
Для чтения документации к проекту можно выбрать следующие варианты:
1. модуль openapi.json из директории проекта вставить в upload file на сайте https://redocly.github.io/redoc/
2. запустить проект командой app.main:app, открыть uri по локальному адресу http://127.0.0.1:8000/docs

### Процесс инвестирования 
В app/services/investment.py корутины exc_status_note и investing - выполняют следующую задачу:

Сразу после создания нового проекта или пожертвования должен запускаться процесс «инвестирования» (увеличение invested_amount как в пожертвованиях, так и в проектах, установка значений fully_invested и close_date, при необходимости). 
Если создан новый проект, а в базе были «свободные» (не распределённые по проектам) суммы пожертвований — они автоматически должны инвестироваться в новый проект*, и в ответе API эти суммы должны быть учтены. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования должны автоматически зачислиться на их счета.

*Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

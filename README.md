# Django Блог

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-brightgreen.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Полнофункциональный блог на Django с аутентификацией, CRUD операциями, поиском и темами оформления.

![Скриншот блога](screenshot.png)

## Особенности

- 🚀 CRUD для постов
- 🔐 Аутентификация пользователей
- 🌙 Темная/светлая тема
- 🔍 Поиск по контенту
- 📱 Адаптивный дизайн
- 📄 Пагинация постов
- ✨ Современный UI

## Технологии

- **Backend:** Django 5.2
- **Frontend:** HTML5, CSS3, JS
- **Database:** SQLite (PostgreSQL готов к продакшн)
- **Дополнительно:**
    - Django Auth System
    - Django ORM
    - Django Pagination
      Основные функции
      Главная: Список постов с пагинацией

## Основные функции

- **Главная**: Список постов с пагинацией
- **Создать пост**: `/post/new/` (требуется вход)
- **Редактировать**: `/post/<id>/edit/` (только автор)
- **Поиск**: `/search/?q=запрос`
- **Профиль**: Базовая информация пользователя
- **Админка**: `/admin` (требует суперпользователя)

## Планы развития

- Комментарии и лайки
- Подписки на авторов
- REST API
- Уведомления
- Восстановление пароля

## Структура проекта

myblog/

├── blog/ # Основное приложение

├── users/ # Аутентификация

├── myblog/ # Настройки проекта

├── .gitignore

├── manage.py

├── README.md

└── requirements.txt

**Лицензия:** [MIT](LICENSE)  
**Автор:** Батраз Секинаев   
**Email:** bsekinaev@ya.ru  
**GitHub:** @bsekinaev


## Быстрый старт

```bash
git clone https://github.com/ваш-пользователь/ваш-репозиторий.git
cd myblog
python -m venv venv
# Linux/Mac: source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Опционально
python manage.py runserver
Открыть в браузере: http://localhost:8000



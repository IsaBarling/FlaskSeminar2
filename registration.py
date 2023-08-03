import re
import json
import hashlib
import os
from flask import request, redirect, url_for

# Путь к файлу, в котором будут храниться данные пользователей
USERS_DATA_FILE = 'D:/Github5/my_online_store/users_data.json'

# Предположим, у нас есть словарь для хранения данных пользователей
users = {}


# Функция для проверки валидности адреса электронной почты
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)


# Функция для хеширования пароля
def hash_password(password):
    # Выбираем алгоритм хеширования (SHA-256)
    sha256 = hashlib.sha256()
    # Преобразуем пароль в байтовую строку перед хешированием
    password = password.encode('utf-8')
    sha256.update(password)
    # Возвращаем хеш пароля в виде строкового значения в шестнадцатеричном формате
    return sha256.hexdigest()


# Функция для сохранения данных пользователей в файл JSON
def save_users_to_json(users_data):
    with open(USERS_DATA_FILE, 'w') as f:
        json.dump(users_data, f)


# Функция для загрузки данных пользователей из файла JSON
def load_users_from_json():
    try:
        with open(USERS_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файл не найден, возвращаем пустой словарь
        return {}


# Загружаем данные пользователей из файла JSON при старте приложения
users = load_users_from_json()


def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Проверка на уникальность адреса почты
        if email in users:
            return "Пользователь с таким адресом почты уже зарегистрирован!"

        # Проверка на валидность адреса почты
        if not is_valid_email(email):
            return "Неверный формат адреса электронной почты!"

        # Проверка на длину пароля
        if len(password) < 8:
            return "Пароль должен содержать минимум 8 символов!"

        # Хешируем пароль
        hashed_password = hash_password(password)

        # Сохранение данных пользователя в словаре
        users[email] = hashed_password

        # Сохраняем обновленные данные пользователей в файл JSON
        save_users_to_json(users)

        # Перенаправление на главную страницу после успешной регистрации
        return redirect(url_for('index'))

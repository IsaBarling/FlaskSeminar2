from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import os
from feedback_data import generate_feedback_number, save_feedback_to_json, save_receipt_photo
from registration import save_users_to_json, hash_password, is_valid_email

app = Flask(__name__)
app.debug = True

# Установка секретного ключа
app.secret_key = 'your_secret_key_here'

# Предположим, у нас есть словарь для хранения данных пользователей
users = {}

# Предположим, у нас есть данные о предметах в каждой категории
clothes_data = [
    {'name': 'Пижама1', 'color': 'красный', 'price': 500},
    {'name': 'Пижама2', 'color': 'синий', 'price': 700},
]

kids_clothes_data = [
    {'name': 'Пижама1', 'color': 'черный', 'price': 1500},
    {'name': 'Пижама2', 'color': 'коричневый', 'price': 1000},
]

men_clothes_data = [
    {'name': 'Пижама1', 'color': 'черный', 'price': 2500},
    {'name': 'Пижама2', 'color': 'серый', 'price': 1800},
]


@app.route('/')
def index():
    # Чтение содержимого файла story.txt
    with open('D:/Github5/my_online_store/story.txt', 'r', encoding='utf-8') as file:
        story_text = file.read()

    return render_template('index.html', title='Главная', story_text=story_text)


@app.route('/welcome/')
def welcome():
    # Получение данных из cookie, если они есть
    user_name = request.cookies.get('user_name')
    user_email = request.cookies.get('user_email')

    # Если данные отсутствуют, перенаправление на страницу ввода
    if not user_name or not user_email:
        return redirect(url_for('register_route'))

    return render_template('welcome.html', title='Добро пожаловать,', user_name=user_name)


@app.route('/register/', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        name = request.form['name']
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
        users[email] = {
            'name': name,
            'password': hashed_password,
        }

        # Сохраняем обновленные данные пользователей в файл JSON
        save_users_to_json(users)

        # Создание cookie с данными пользователя
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)

        return response

    return render_template('register.html', title='Регистрация')


@app.route('/profile/')
def profile():
    # Получение данных из cookie, если они есть
    user_name = request.cookies.get('user_name')

    # Если данные отсутствуют, перенаправление на страницу ввода
    if not user_name:
        return redirect(url_for('register_route'))

    return render_template('profile.html', title='Профиль', user_name=user_name)


@app.route('/logout/')
def logout():
    # Удаление cookie с данными пользователя
    response = make_response(redirect(url_for('register_route')))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')

    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Здесь можно добавить логику проверки наличия пользователя в базе данных и соответствия пароля

        # Перенаправление на главную страницу после успешного входа
        return redirect(url_for('index'))

    return render_template('login.html', title='Вход')


@app.route('/catalog/')
def catalog_route():
    return render_template('catalog.html', title='Каталог товаров', clothes_data=clothes_data, kids_clothes_data=kids_clothes_data, men_clothes_data=men_clothes_data)


@app.route('/feedback/', methods=['GET', 'POST'])
def feedback_route():
    if request.method == 'POST':
        # Ваша логика обработки данных обратной связи
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        passport_data = request.form['passport_data']
        purchase_data = request.form['purchase_data']
        receipt_photo = request.files['receipt_photo']

        # Генерация уникального номера для жалобы
        feedback_number = generate_feedback_number()

        # Папка для хранения данных жалобы
        feedback_folder = f"D:/Github5/my_online_store/receipt_photos/{feedback_number}"

        # Сохранение фото чека и получение пути к сохраненному файлу
        receipt_photo_path = save_receipt_photo(receipt_photo, feedback_folder)

        # Сохранение данных обратной связи в файл JSON
        feedback_data = {
            'feedback_number': feedback_number,
            'name': name,
            'surname': surname,
            'patronymic': patronymic,
            'passport_data': passport_data,
            'purchase_data': purchase_data,
            # Здесь также можно добавить другие данные, если необходимо
        }
        save_feedback_to_json(feedback_data, feedback_folder)

        # Отправляем флэш-сообщение пользователю
        flash("Ваша жалоба получена. Мы уже ее рассматриваем", "success")

        # Перенаправление на страницу обратной связи после отправки данных
        return redirect(url_for('feedback_route'))

    return render_template('feedback.html', title='Обратная связь')


if __name__ == '__main__':
    app.run()

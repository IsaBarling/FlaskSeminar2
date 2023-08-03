from flask import request, redirect, url_for

def feedback():
    if request.method == 'POST':
        # Обработка данных обратной связи
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        passport_data = request.form['passport_data']
        purchase_data = request.form['purchase_data']
        receipt_photo = request.files['receipt_photo']
        # (Здесь можно сохранить данные в базу данных или обработать каким-либо другим способом)

        # Перенаправление на страницу обратной связи после отправки данных
        return redirect(url_for('feedback'))

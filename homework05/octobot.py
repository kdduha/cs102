import json
import re
from datetime import datetime

# некоторые импорты ломаются в mypy, вкратце оф.документация говорит. что лучший вариант - прописать ignore
# https://mypy.readthedocs.io/en/stable/running_mypy.html
import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6147995148:AAGra_H1gb-dwfUuZLmtCU8QtjLmVoqwm98")


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    # PUT YOUR CODE HERE
    if divider != date[2]:
        return False
    try:
        converted_date = datetime.strptime("/".join(date.split(divider)), "%d/%m/%y")
    except ValueError:
        # проверка на существование даты в календаре
        return False

    if -1 <= (converted_date - datetime.today()).days < 365 and converted_date.date() >= datetime.today().date():
        return True
    return False


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    # PUT YOUR CODE HERE
    if "https://" not in url and "http://" not in url:
        url = "https://" + url
    try:
        if requests.get(url).status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    # PUT YOUR CODE HERE
    return datetime.strptime(date, "%d/%m/%y")


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    if is_valid_url(url):
        sheet_id = url.split("/")[url.split("/").index("d") + 1]  # sheet_id
        try:
            with open("tables.json") as json_file:
                tables = json.load(json_file)
            title = len(tables) + 1
            tables[title] = {"url": url, "id": sheet_id}
        except FileNotFoundError:
            tables = {0: {"url": url, "id": sheet_id}}
        with open("tables.json", "w") as json_file:
            json.dump(tables, json_file)
        bot.send_message(message.chat.id, "Таблица подключена!")
    else:
        bot.send_message(message.chat.id, "Простите, вы ввели неккоректный url :(")
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        # PUT YOUR CODE HERE
        info = bot.send_message(message.chat.id, "Дайте ссылку на google-таблицу.")
        bot.register_next_step_handler(info, connect_table)

    elif message.text == "Редактировать предметы":
        # PUT YOUR CODE HERE
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить предмет")
        start_markup.row("Изменить название и url предмета")
        start_markup.row("Удалить предмет")
        start_markup.row("Очистить всю таблицу")
        start_markup.row("Главное меню")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)

    elif message.text == "Редактировать дедлайны":
        # PUT YOUR CODE HERE
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadline_markup.row("Добавить новый дедлайн")
        deadline_markup.row("Изменить дедлайн")
        deadline_markup.row("Удалить дедлайн")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=deadline_markup)
        bot.register_next_step_handler(info, choose_deadline_action)

    elif message.text == "Посмотреть дедлайны на этой неделе":
        # PUT YOUR CODE HERE
        show_deadlines(message)

    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды :(")
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    # PUT YOUR CODE HERE
    if message.text == "Удалить предмет":
        info = bot.send_message(message.chat.id, "Напишите название предмета, который хотите удалить.")
        bot.register_next_step_handler(info, delete_subject)

    elif message.text == "Изменить название и url предмета":

        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        df = access_current_sheet()[2]

        for subject in df["Subject"]:
            start_markup.row(subject)
        start_markup.row("Главное меню")

        info = bot.send_message(
            message.chat.id, "Нажмите на название предмета, который хотите изменить.", reply_markup=start_markup
        )
        bot.register_next_step_handler(info, update_subject)

    elif message.text == "Добавить предмет":
        info = bot.send_message(message.chat.id, "Напишите название нового предмета.")
        bot.register_next_step_handler(info, add_new_subject)

    elif message.text == "Очистить всю таблицу":
        choose_removal_option(message)

    elif message.text == "Главное меню":
        start(message)

    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды :(")
        start(message)


def show_deadlines(message):
    worksheet, _, df = access_current_sheet()
    text_table = []
    for index in range(df.shape[0]):
        sub = df["Subject"][index]
        link = df["Link"][index] if df["Link"][index] else "<нет>"
        text = f"#{index} Предмет: {sub}\nСсылка: {link}\nДедлайны:"
        d = df.loc[:, "1":"5"]
        dates_text = ""
        for i in range(1, d.shape[1] + 1):
            if d[str(i)][index]:
                date = d[str(i)][index]
                date = convert_date("/".join(date.split(date[2])))
                today = datetime.today()

                if date >= today and (date - today).days <= 7:
                    dates_text += f"          {i} работа >> {d[str(i)][index]} !!! НА ЭТОЙ НЕДЕЛЕ !!!\n"
                else:
                    dates_text += f"          {i} работа >> {d[str(i)][index]}\n"

        text = f"{text}\n{dates_text}" if dates_text else text + " <нет>"
        text_table.append(text)

    bot.send_message(message.chat.id, "\n\n".join(text_table))
    start(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    # PUT YOUR CODE HERE
    if message.text == "Удалить дедлайн":
        info = bot.send_message(
            message.chat.id, "Напишите через запятую название предмета и номер работы, у которой хотите убрать дедлайн."
        )
        bot.register_next_step_handler(info, delete_deadline)

    elif message.text == "Изменить дедлайн":

        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        df = access_current_sheet()[2]

        for subject in df["Subject"]:
            start_markup.row(subject)
        start_markup.row("Главное меню")

        info = bot.send_message(
            message.chat.id,
            "Нажмите на название предмета, у которого хотите изменить дедлайн.",
            reply_markup=start_markup,
        )
        bot.register_next_step_handler(info, choose_subject)

    elif message.text == "Добавить новый дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        df = access_current_sheet()[2]

        for subject in df["Subject"]:
            start_markup.row(subject)
        start_markup.row("Главное меню")

        info = bot.send_message(
            message.chat.id,
            "Нажмите на название предмета, у которого хотите добавить дедлайн.",
            reply_markup=start_markup,
        )
        bot.register_next_step_handler(info, choose_subject)

    elif message.text == "Главное меню":
        start(message)

    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды :(")
        start(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    # PUT YOUR CODE HERE
    warning = bot.send_message(message.chat.id, "Вы точно хотите удалить таблицу? (да/нет)")
    bot.register_next_step_handler(warning, clear_subject_list)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    # PUT YOUR CODE HERE
    worksheet, _, df = access_current_sheet()
    old_sub = message.text

    if not df["Subject"].isin([old_sub]).any():
        print(df["Subject"], old_sub)
        bot.send_message(message.chat.id, "Такого предмета нет!")
        return start(message)
    if old_sub == "Главное меню":
        return start(message)

    info = bot.send_message(message.chat.id, "Напишите через запятую номер работы и новый дедлайн (dd/mm/yy).")
    bot.register_next_step_handler(info, update_subject_deadline, message.text)


def update_subject_deadline(msg, old_sub):
    """Обновляем дедлайн"""
    # PUT YOUR CODE HERE
    worksheet, _, df = access_current_sheet()
    try:
        n, date = [el.strip() for el in msg.text.split(",")]
        if not 1 <= int(n) <= 5:
            bot.send_message(msg.chat.id, "Номер работы должен быть числом между 1 и 5.")
            return start(msg)

        if is_valid_date(date, date[2]):
            updated_subject_row = worksheet.find(old_sub).row
            date = convert_date("/".join(date.split(date[2])))
            worksheet.update_cell(updated_subject_row, int(n) + 2, date.strftime("%d/%m/%y"))
            bot.send_message(msg.chat.id, "Обновление прошло успешно!")
            start(msg)
        else:
            bot.send_message(
                msg.chat.id,
                "Вы неккоректно ввели дату :( Проверьте, что она существует, релевантна или правильно набрана.",
            )
            start(msg)
    except ValueError:
        bot.send_message(
            msg.chat.id, "Вводите новые данные через запятую -.- Также номер работы должен быть числом между 1 и 5."
        )
        start(msg)


def delete_deadline(msg):
    """Вносим новое название предмета в Google-таблицу"""
    # PUT YOUR CODE HERE

    worksheet, _, df = access_current_sheet()
    try:
        sub, n = [el.strip() for el in msg.text.split(",")]
        if not df["Subject"].isin([sub]).any():
            bot.send_message(msg.chat.id, "Такого предмета нет.")
            return start(msg)

        if not 1 <= int(n) <= 5:
            bot.send_message(msg.chat.id, "Номер работы должен быть числом между 1 и 5.")
            return start(msg)

        worksheet.update_cell(worksheet.find(sub).row, int(n) + 2, "")
        bot.send_message(msg.chat.id, f"Дедлайн удален.")
        start(msg)

    except ValueError:
        bot.send_message(
            msg.chat.id, "Вводите новые данные через запятую -.- Также номер работы должен быть числом между 1 и 5."
        )
        start(msg)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    # PUT YOUR CODE HERE
    worksheet, _, df = access_current_sheet()

    if df["Subject"].isin([message.text]).any():
        bot.send_message(message.chat.id, "Такой предмет уже есть.")
        return start(message)

    worksheet.append_row([message.text])
    info = bot.send_message(message.chat.id, "Добавьте url предмета.")
    bot.register_next_step_handler(info, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    # PUT YOUR CODE HERE
    if is_valid_url(message.text):
        worksheet, _, df = access_current_sheet()
        index_row = df.shape[0] + 1
        worksheet.update_cell(index_row, 2, message.text)

        bot.send_message(message.chat.id, "Данные успешно внесены.")
        start(message)

    else:
        bot.send_message(message.chat.id, "Ссылка некорректна.")
        start(message)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    # PUT YOUR CODE HERE
    worksheet, _, df = access_current_sheet()
    old_sub = message.text

    if not df["Subject"].isin([old_sub]).any():
        bot.send_message(message.chat.id, "Такого предмета нет!")
        return start(message)
    if old_sub == "Главное меню":
        return start(message)

    def new_subject_and_url(msg):
        try:
            sub, url = [el.strip() for el in msg.text.split(",")]
            if is_valid_url(url):
                updated_subject_row = worksheet.find(old_sub).row
                worksheet.update_cell(updated_subject_row, 1, sub)
                worksheet.update_cell(updated_subject_row, 2, url)
                bot.send_message(msg.chat.id, "Обновление прошло успешно!")
                start(msg)
            else:
                bot.send_message(msg.chat.id, "Вы ввели неккоректный url :( Будьте внимательнее!")
                start(msg)
        except ValueError:
            bot.send_message(msg.chat.id, "Вводите новые данные через запятую -.-")
            start(msg)

    info = bot.send_message(message.chat.id, "Напишите через запятую новое название и новый url.")
    bot.register_next_step_handler(info, new_subject_and_url)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    # PUT YOUR CODE HERE
    worksheet, _, df = access_current_sheet()
    if not df["Subject"].isin([message.text]).any():
        bot.send_message(message.chat.id, "Такого предмета нет!")
        return start(message)
    worksheet.delete_row(worksheet.find(message.text).row)
    bot.send_message(message.chat.id, f"Предмет {message.text} удален.")
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    # PUT YOUR CODE HERE
    if message.text.lower() == "да":
        worksheet = access_current_sheet()[0]
        worksheet.batch_clear(["A2:A", "B2:B", "C2:C", "D2:D", "E2:E", "F2:F", "G2:G"])
        bot.send_message(message.chat.id, "Таблица удалена (очищена).")
        start(message)

    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id, "Вы отменили удаление таблицы.")
        start(message)

    else:
        bot.send_message(message.chat.id, "Введите только да/нет! Давайте еще раз.")
        bot.register_next_step_handler(message, clear_subject_list)


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайны")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


# bot.infinity_polling()

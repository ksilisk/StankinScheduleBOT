# -*- coding: utf-8 -*-
from telebot.async_telebot import AsyncTeleBot
from datetime import datetime, timedelta
from telebot import types
import aioschedule
import dateparser as p
import SQLLib as sql
import asyncio
import json


API_TOKEN = "973541236:AAFLvoGUV1btTIYuoJ8i4NxXv2K4gGrQiBY"
bot = AsyncTeleBot(API_TOKEN)

GROUPS = ['АДБ-18-01', 'АДБ-18-02', 'АДБ-18-03', 'АДБ-18-06', 'АДБ-18-07', 'АДБ-18-08', 'АДБ-18-09', 'АДБ-18-10',
          'АДБ-18-11', 'АДБ-19-01', 'АДБ-19-02', 'АДБ-19-03', 'АДБ-19-06', 'АДБ-19-07', 'АДБ-19-08', 'АДБ-19-09',
          'АДБ-19-10', 'АДБ-19-11', 'АДБ-20-01', 'АДБ-20-02', 'АДБ-20-03', 'АДБ-20-06', 'АДБ-20-07', 'АДБ-20-08',
          'АДБ-20-09', 'АДБ-20-10', 'АДБ-20-11', 'АДБ-20-12', 'АДБ-21-01', 'АДБ-21-02', 'АДБ-21-03', 'АДБ-21-04',
          'АДБ-21-06', 'АДБ-21-07', 'АДБ-21-08', 'АДБ-21-09', 'АДБ-21-10', 'АДБ-21-11', 'АДМ-20-03', 'АДМ-20-04',
          'АДМ-21-01', 'АДМ-21-02', 'АДМ-21-03', 'АДМ-21-04', 'АДМ-21-05', 'АДМ-21-06', 'АСП-19-01(09-01)',
          'АСП-19-01(09-02)', 'АСП-19-02(15-01)', 'АСП-19-02(15-02)', 'АСП-19-02(15-03)', 'АСП-20-01',
          'АСП-20-02(15-01)', 'АСП-20-02(15-02)', 'АСП-20-03', 'АСП-21-01', 'АСП-21-02', 'АСП-21-03', 'ИДБ-18-01',
          'ИДБ-18-02', 'ИДБ-18-03', 'ИДБ-18-04', 'ИДБ-18-05', 'ИДБ-18-06', 'ИДБ-18-07', 'ИДБ-18-08', 'ИДБ-18-09',
          'ИДБ-18-10', 'ИДБ-18-11', 'ИДБ-19-01', 'ИДБ-19-02', 'ИДБ-19-04', 'ИДБ-19-05', 'ИДБ-19-06', 'ИДБ-19-07',
          'ИДБ-19-08', 'ИДБ-19-09', 'ИДБ-19-10', 'ИДБ-19-11', 'ИДБ-20-01', 'ИДБ-20-02', 'ИДБ-20-03', 'ИДБ-20-04',
          'ИДБ-20-05', 'ИДБ-20-06', 'ИДБ-20-07', 'ИДБ-20-08', 'ИДБ-20-09', 'ИДБ-20-10', 'ИДБ-20-11', 'ИДБ-21-01',
          'ИДБ-21-02', 'ИДБ-21-03', 'ИДБ-21-04', 'ИДБ-21-05', 'ИДБ-21-06', 'ИДБ-21-07', 'ИДБ-21-08', 'ИДБ-21-09',
          'ИДБ-21-10', 'ИДБ-21-11', 'ИДБ-21-12', 'ИДМ-20-01', 'ИДМ-20-02', 'ИДМ-20-03(ИГ)', 'ИДМ-20-03(ПрМ)',
          'ИДМ-20-03(ФМ)', 'ИДМ-20-04', 'ИДМ-20-05', 'ИДМ-20-06', 'ИДМ-21-01', 'ИДМ-21-02', 'ИДМ-21-03(ИГ)',
          'ИДМ-21-03(ПрМ)', 'ИДМ-21-03(ФМ)', 'ИДМ-21-04', 'ИДМ-21-05', 'ИДМ-21-06', 'ИДМ-21-07', 'ИДМ-21-08',
          'МДБ-18-03', 'МДБ-18-04', 'МДБ-18-05', 'МДБ-18-06', 'МДБ-18-07', 'МДБ-18-08', 'МДБ-19-03', 'МДБ-19-04',
          'МДБ-19-05', 'МДБ-19-06', 'МДБ-19-07', 'МДБ-19-09', 'МДБ-19-10', 'МДБ-20-03', 'МДБ-20-04', 'МДБ-20-05',
          'МДБ-20-06', 'МДБ-20-07', 'МДБ-20-09', 'МДБ-20-10', 'МДБ-20-12', 'МДБ-21-03(02)', 'МДБ-21-03(05)',
          'МДБ-21-04', 'МДБ-21-05', 'МДБ-21-06', 'МДБ-21-07', 'МДБ-21-09', 'МДМ-20-01', 'МДМ-20-02', 'МДМ-20-03',
          'МДМ-20-04(СПД)', 'МДМ-20-04(СТ)', 'МДМ-20-06', 'МДМ-20-07', 'МДМ-21-01(КМ)', 'МДМ-21-01(ТМ)', 'МДМ-21-02',
          'МДМ-21-03', 'МДМ-21-04(СПД)', 'МДМ-21-04(СТ)', 'МДМ-21-06', 'МДМ-21-07', 'МДМ-21-11', 'МДМ-21-12',
          'МДС-17-01', 'МДС-17-02', 'МДС-18-01', 'МДС-18-02', 'МДС-19-01', 'МДС-19-02', 'МДС-20-01', 'МДС-20-02',
          'МДС-20-11', 'МДС-21-01', 'МДС-21-02', 'МДС-21-11', 'ЭВМ-20-01(МВБ)', 'ЭВМ-20-01(УЧР)', 'ЭВМ-20-01(ФМ)',
          'ЭВМ-21-01(ГМУ)', 'ЭВМ-21-01(МВБ)', 'ЭВМ-21-01(УП)', 'ЭВМ-21-01(УЧР)', 'ЭВМ-21-01(ФМ)', 'ЭДБ-18-01',
          'ЭДБ-18-02(ПМ)', 'ЭДБ-18-02(УПр)', 'ЭДБ-18-03', 'ЭДБ-18-04', 'ЭДБ-18-05', 'ЭДБ-19-01', 'ЭДБ-19-02(УП)',
          'ЭДБ-19-02(УПр)', 'ЭДБ-19-03', 'ЭДБ-19-05', 'ЭДБ-19-06', 'ЭДБ-20-01(ИН)', 'ЭДБ-20-01', 'ЭДБ-20-02(УП)',
          'ЭДБ-20-02(УПр)', 'ЭДБ-20-02(УЧР)', 'ЭДБ-20-05', 'ЭДБ-20-08', 'ЭДБ-21-01', 'ЭДБ-21-02(02)', 'ЭДБ-21-02(03)',
          'ЭДБ-21-03', 'ЭДБ-21-05', 'ЭДБ-21-06', 'ЭДБ-21-09', 'ЭДБ-21-10', 'ЭДМ-20-02(МВБ)', 'ЭДМ-20-02(УЧР)',
          'ЭДМ-20-02(ФМ)', 'ЭДМ-20-05', 'ЭДМ-21-02(ГМУ)', 'ЭДМ-21-02(МВБ)', 'ЭДМ-21-02(УП)', 'ЭДМ-21-02(УЧР)',
          'ЭДМ-21-02(ФМ)', 'ЭДМ-21-04', 'ЭДМ-21-05', 'ЭДМ-21-08', 'ЭДМ-21-09']


@bot.message_handler(commands=['start'])
async def start(message):  # отправить сообщение со списком всех груп
    if sql.check_user(message.chat.id):
        sql.del_user(message.chat.id)
    sql.add_user(message.chat.id)
    await bot.send_message(message.chat.id, 'Отправьте название своей группы!\n(Например - "ИДБ-21-09")\nСписок групп можно '
                                      'посмотреть <a href="https://drive.google.com/file/d'
                                      '/1jRj7Ru8fF3TioJc5JZ46512yr4YWR6ul/view?usp=sharing">тут</a>',
                     parse_mode='HTML',
                     disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
async def message_hand(message):
    state = sql.get_state(message.chat.id)
    if state == '/start':
        await add_group(message.chat.id, message.text)
    elif state == 'group_choice':
        await group_choice(message.chat.id, message.text)
    elif state == 'time_send':
        await time_send(message.chat.id, message.text)
    elif state == 'add_time':
        await add_time(message.chat.id, message.text)



@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if '_' in call.data:
        if call.data.split('_')[0] == 'group':
            await edit_schedule(datetime.today(), call.from_user.id, call.data.split('_')[1], call.message.id)
        else:
            await edit_schedule(p.parse(call.data.split('_')[0]), call.from_user.id, call.data.split('_')[1],
                                call.message.id)


async def add_time(user_id, time_to_send):
    if ((0 <= int(time_to_send.split(':')[0]) <= 23) and (0 <= int(time_to_send.split(':')[1]) <= 59)):
        await bot.send_message(user_id, 'ok') # сделать добавление события через aioschedule для пользователя
        await send_schedule(datetime.today(),user_id) # и отправить расписание
    else:
        await bot.send_message(user_id, 'Пожалуйста, введите корректное значение!')


async def time_send(user_id, text):
    if text == 'Да':
        await bot.send_message(user_id, 'Отправьте время, когда бот должен присылать Вам расписание!\n(Например, 12:30)')
        sql.set_state(user_id, 'add_time')
    elif text == 'Нет':
        await send_schedule(datetime.today(), user_id)
    else:
        await bot.send_message(user_id, 'Пожалуйста, введите корректное значение!',
                               reply_markup=types.ReplyKeyboardMarkup(True,True).row(
                                   types.KeyboardButton('Да'),
                                   types.KeyboardButton('Нет')))

async def group_choice(user_id, text):
    if text == 'Да':
        await bot.send_message(user_id, 'Пришлите название группы!')
        sql.set_state(user_id, '/start')
    elif text == 'Нет':
        await bot.send_message(user_id, 'Хотите ли Вы получать расписание ежедневно в какое-то время?',
                               reply_markup=types.ReplyKeyboardMarkup(True, True).row(
                                   types.KeyboardButton('Да'),
                                   types.KeyboardButton('Нет')))
        sql.set_state(user_id, 'time_send')
    else:
        await bot.send_message(user_id, 'Пожалуйста, введите корректное значение!')


async def add_group(user_id, text):
    if text in GROUPS:
        sql.add_group(user_id, text)
        markup = types.ReplyKeyboardMarkup(True, True).row(types.KeyboardButton('Да'),
                                                           types.KeyboardButton('Нет'))
        if sql.get_groups_count(user_id) < 3:
            await bot.send_message(user_id, 'Отлично!\nХотите добавить еще одну группу? (не больше 3-х)',
                                   reply_markup=markup)
            sql.set_state(user_id, 'group_choice')
        else:
            await bot.send_message(user_id, 'Хотите ли Вы получать расписание ежедневно в какое-то время?',
                                   reply_markup=markup)
            sql.set_state(user_id, 'time_send')
    else:
        await bot.send_message(user_id,
                         'Такой группы в базе нет!\nПроверьте правильность сообщения и попробуйте снова!')


async def send_schedule(date, user_id):
    user_groups = sql.get_groups(user_id).split(' ')
    button_list = [[], []]
    button_list[0].extend(
        [types.InlineKeyboardButton('<-', callback_data=str(date - timedelta(days=1)) + '_' + user_groups[0]),
         types.InlineKeyboardButton('->', callback_data=str(date + timedelta(days=1)) + '_' + user_groups[0])])
    for u_group in user_groups:
        if u_group != user_groups[0]:
            button_list[1].append(types.InlineKeyboardButton(u_group, callback_data='group_' + u_group))
    markup = types.InlineKeyboardMarkup(button_list, row_width=3)
    schedule = await get_schedule(user_groups[0], date)
    await bot.send_message(user_id, schedule, reply_markup=markup, parse_mode='HTML')
    sql.set_state(user_id, 'schedule')


async def edit_schedule(date, user_id, user_group, message_id):
    user_groups = sql.get_groups(user_id).split(' ')
    button_list = [[], []]
    if date.date() == datetime.today().date():
        button_list[0].extend(
            [types.InlineKeyboardButton('<-', callback_data=str(date - timedelta(days=1)) + '_' + user_group),
             types.InlineKeyboardButton('->', callback_data=str(date + timedelta(days=1)) + '_' + user_group)])
    else:
        button_list[0].extend(
            [types.InlineKeyboardButton('<-', callback_data=str(date - timedelta(days=1)) + '_' + user_group),
             types.InlineKeyboardButton('Сегодня', callback_data=str(datetime.today()) + '_' + user_group),
             types.InlineKeyboardButton('->', callback_data=str(date + timedelta(days=1)) + '_' + user_group)])

    for u_group in user_groups:
        if u_group != user_group:
            button_list[1].append(types.InlineKeyboardButton(u_group, callback_data='group_' + u_group))
    markup = types.InlineKeyboardMarkup(button_list, row_width=3)
    schedule = await get_schedule(user_group, date)
    await bot.edit_message_text(schedule, user_id, message_id, reply_markup=markup, parse_mode='HTML')


async def get_schedule(group, date):
    weekdays = ['Понедельник ', 'Вторник ', 'Среда ', 'Четверг ', 'Пятница ', 'Суббота ', 'Воскресенье ']
    schedule = group + '\n<b>' + weekdays[date.weekday()] + '</b>' + str(date.date()) \
               + '\n<b>-------------------------------------------</b>\n'
    lessons_list = []
    file = open('schedules/' + group + '.json', 'r').read()
    lessons = json.loads(file)
    for lesson in lessons:
        for lesson_date in lesson['dates']:
            if lesson_date['frequency'] == 'once' and date == p.parse(lesson_date['date']).date():
                lessons_list.append(lesson)
            elif lesson_date['frequency'] == 'every' and p.parse(
                    lesson_date['date'].split('-')[0]).date() <= date.date() <= p.parse(
                lesson_date['date'].split('-')[1]).date() and date.weekday() == p.parse(
                lesson_date['date'].split('-')[0]).date().weekday():
                lessons_list.append(lesson)
            elif lesson_date['frequency'] == 'throughout':
                start_date = p.parse(lesson_date['date'].split('-')[0]).date()
                end_date = p.parse(lesson_date['date'].split('-')[1]).date()
                delta = timedelta(weeks=2)
                while start_date != end_date:
                    start_date = start_date + delta
                    if start_date == date.date():
                        lessons_list.append(lesson)
                        break
    if not lessons_list:
        return schedule
    lessons_list = sorted(lessons_list, key=lambda temp: temp['time']['end'])
    for s in lessons_list:
        if s['subgroup'] == 'Common':
            s['subgroup'] = 'Вся группа'
        schedule += '<u>' + s['title'] + '</u>\n<i>' + s['lecturer'] + '</i>\n' + s['classroom'] + '\n<b>' \
                    + s['type'] + '</b>\n' + s['subgroup'] + '\n' \
                    + s['time']['start'] + ' - ' + s['time']['end'] + '\n'
        schedule += '<b>--------------------------------------------</b>\n'
    return schedule


async def main():
    await asyncio.gather(bot.infinity_polling())


if __name__ == '__main__':
    asyncio.run(main())

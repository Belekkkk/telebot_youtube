import os
import telebot
from telebot import types
from pytube import YouTube


bot = telebot.TeleBot('7085058616:AAHfKQ1He-nahOhuF88fdzwLILcb8YSng7w')
video_url = ''



def get_url_data(message):
    global video_url
    video_url = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_video = types.InlineKeyboardButton(text='Видео', callback_data='video')
    key_audio = types.InlineKeyboardButton(text='Аудио', callback_data='audio')
    keyboard.add(key_video)
    keyboard.add(key_audio)
    bot.send_message(message.from_user.id, 'Выбери тип загрузки', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Привет, скинь мне ссылку с youtube и я конвертирую его в mp3 или в mp4')
        bot.register_next_step_handler(message, get_url_data)
    else:
        bot.send_message(message.from_user.id, 'напиши /start чтобы начать')


@bot.callback_query_handler(func=lambda call: True)
def get_audio_and_video(call):
    yt = YouTube(video_url)
    bot.send_message(call.message.chat.id, 'Запрос обрабатывается...Вейт')
    if call.data == 'video':
        source = yt.streams.first()
        cwd = os.getcwd()
        out_file = source.download(output_path=cwd)
        video_file = open(out_file, 'rb')
        bot.send_video(call.message.chat.id, video_file)
    elif call.data == 'audio':
        source = yt.streams.filter(only_audio=True).first()
        cwd = os.getcwd()
        out_file = source.download(output_path=cwd)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        bot.send_audio(call.message.chat.id, open(new_file, 'rb'))

bot.polling(non_stop=True, interval=0)
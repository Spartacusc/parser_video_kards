from aiogram import utils, types
from peewee import *

db = SqliteDatabase('videocards.db')


class BaseModel(Model):
    class Meta:
        database = db


class VideoCard(BaseModel):
    title = CharField()
    url = TextField()


class SearchModel(BaseModel):
    title = CharField()
    chat_id = CharField()


def find_all_cards():
    return VideoCard.select()


def find_id_search(chat_id):
    return SearchModel.select().where(SearchModel.chat_id == chat_id)


def find_all_search():
    return SearchModel.select()


async def process_search_model(message):
    search_exist = True
    try:
        search = SearchModel.select().where(SearchModel.title == message.text).get()
        search.delete_instance()
        await message.answer(f'Строка поиска {message.text} удалена')
        return search_exist
    except DoesNotExist as de:
        search_exist = False

    if not search_exist:
        rec = SearchModel(title=message.text, chat_id=message.chat.id)
        rec.save()
        await message.answer(f'Строка поиска {message.text} добавлена')
    else:
        await message.answer(f'Строка поиска {message.text} уже есть')
    return search_exist


async def add_video_card(title, url, chat_id, bot):
    card_exist = True
    try:
        card = VideoCard.select().where(VideoCard.title == title).get()
    except DoesNotExist as de:
        card_exist = False

    if not card_exist:
        rec = VideoCard(title=title, url=url)
        rec.save()
        message_text = utils.markdown.hlink(title, url)
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=types.ParseMode.HTML)
    return card_exist


def init_db():
    db.create_tables([VideoCard, SearchModel])

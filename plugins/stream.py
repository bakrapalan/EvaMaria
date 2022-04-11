import asyncio
import base64
import urllib.parse
from pyrogram import Client
import logging
from typing import Any, Optional
from pyrogram import filters
from Vars import Var
from utils import temp
from pyrogram.file_id import FileId
from urllib.parse import quote_plus
from database.ia_filterdb import unpack_new_file_id
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_name", "")

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user

banned_user = filters.create(banned_users)

@Client.on_message( filters.private & ( filters.document | filters.video | filters.audio ) & ~banned_user, group=4,)
async def media_receive_handler(b, m):
    
    banned_user = filters.create(banned_users)
    log_msg = await b.copy_message(chat_id=Var.BIN_CHANNEL, from_chat_id=m.chat.id, message_id=m.message_id)
    stream_link = f"{Var.URL}{log_msg.message_id}/{quote_plus(get_name(m))}?hash={get_hash(log_msg)}"
    short_link = f"{Var.URL}{get_hash(log_msg)}{log_msg.message_id}"
    logging.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    newtext=f"User: **{m.from_user.mention(style='md')}** Track: **#u{m.chat.id}** Hash: **#{get_hash(log_msg)}{log_msg.message_id}** Link: **[Hold Me]({short_link})**"
    
    await m.reply_text(
        text="""<b>🤓 I generated link for you, just reply the file with /link to generate an extra link.</b>""",
        quote=True,
        parse_mode="html", 
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📥 Stream Link', url=f'https://t.me/share/url?url={short_link}')
                    ]
                ]
            )
        )
    await log_msg.edit_text(
        text=f"{newtext}",
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🗑 Delete File', callback_data='delete')
                    ]
                ]
            )
        )
    
EMOJI = ["🎲", "🎯", "🏀", "⚽", "🎳", "🎰", "🎲"]

@Client.on_message(filters.command("emoji"))
async def emoji(bot, message):
    await bot.reply(
    text=random.choice(EMOJI)
    )

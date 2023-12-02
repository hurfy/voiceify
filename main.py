import time

from config    import TELEGRAM_TOKEN
from src.video import download_video, delete_file
from src.cloudflare import CloudflareBucket
from hashlib   import md5
from logging   import basicConfig, INFO
from sys       import stdout
from random    import choice
from asyncio   import run, sleep
from aiogram   import Bot, Dispatcher, types

from aiogram.enums          import ParseMode
from aiogram.filters        import CommandStart
from aiogram.types          import InlineQueryResultVoice, FSInputFile
from aiogram.utils.markdown import hbold

ERRORS = [
       'Huh?🤨',
       'Try writing /start😏',
       'It\'s beautiful weather outside!🌤',
       '404: Wit not found. Try upgrading to Wit 2.0🧠',
       'I\'m fluent in emoji, but your message seems to be written in hieroglyphics. Any translation services '
       'available?🤓',
       'Error 418: I\'m a teapot. Your message is too hot to handle!🍵',
       'Command not recognized. Did you mean to summon a unicorn?🦄',
       'This message is brought to you by the Department of Unintelligible Communications. Can you please speak in '
       'human?👽',
       'Message decryption failed. Are you sure you\'re not a spy from the Secret Society of Puzzling Punctuation?🤪',
       'Error 007: Message too spy-like. Are you James Bond in disguise?🕵️'
]

bucket = CloudflareBucket()
bot    = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp     = Dispatcher()


async def send_ogg_to_local_storage(username: str):
    sent_message = await bot.send_document(chat_id='-4065039756', document=FSInputFile('storage/hurfy-discord.ogg'),
                                        caption=username)

    voice_info = sent_message.document
    file_id = voice_info.file_id
    file_info = await bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

    return file_url


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    :param message: Message: User message
    :return:                 None
    """
    about_msg = (f'Hey, {hbold(message.from_user.full_name)}. I\'m Voiceify Bot! :)\n\n'
                 f'I can record voice messages from the video you send me!\n'
                 f'Just tag me and link to the video in one of your chats.\n\n'
                 f'As of today, I support downloading from these sources:\n'
                 f'* TikTok\n'
                 f'* Instagram\n'
                 f'* YouTube\n'
                 f'* Discord\n'
                 f'* From the direct link to the video')

    await send_ogg_to_local_storage(message.from_user.username)
    await message.answer(about_msg)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    await message.answer(choice(ERRORS))


@dp.inline_query()
async def url_inline_query(query: types.InlineQuery):
    url  = query.query
    user = query.from_user.username

    bucket.upload_file(f'{download_video(user, url)}.ogg', user)
    link = bucket.generate_link(f'{user}.ogg')

    item = InlineQueryResultVoice(
        id=md5(url.encode()).hexdigest(),
        title='Download',
        voice_url=link,
    )

    await bot.answer_inline_query(
        inline_query_id=query.id,
        results=[item],
    )

    await sleep(30)
    delete_file(f'storage/{user}.ogg')
    delete_file(f'storage/{user}.mp4')



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    basicConfig(level=INFO, stream=stdout)
    run(main())

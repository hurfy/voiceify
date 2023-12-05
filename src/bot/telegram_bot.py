from config    import TELEGRAM_TOKEN
from src.utils import ERRORS
from random    import choice
from aiogram   import Bot, Dispatcher, types

from aiogram.enums          import ParseMode
from aiogram.filters        import CommandStart
from aiogram.utils.markdown import hbold


bot    = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp     = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    :param message: Message: User message
    :return:                 None
    """
    # about_msg = (f'Hey, {hbold(message.from_user.full_name)}. I\'m Voiceify Bot! :)\n\n'
    #              f'I can record voice messages from the video you send me!\n'
    #              f'Just tag me and link to the video in one of your chats.\n\n'
    #              f'As of today, I support downloading from these sources:\n'
    #              f'* TikTok\n'
    #              f'* Instagram\n'
    #              f'* YouTube\n'
    #              f'* Discord\n'
    #              f'* From the direct link to the video')

    about_msg = 'WIP for the current moment!'

    await bot.send_message(message.chat.id, text=about_msg)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    await message.answer(choice(ERRORS))

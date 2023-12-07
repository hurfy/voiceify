from src.bot import bot, dp
from asyncio import run
from logging import basicConfig, INFO
from sys     import stdout


async def main() -> None:
    """
    Main function for starting a bot
    :return: None
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        basicConfig(level=INFO, stream=stdout)
        run(main())

    except KeyboardInterrupt:
        print('The bot has successfully completed its work!')

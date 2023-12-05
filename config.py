from decouple import config


def telegram_token() -> str:
    """
    Telegram Token Validation
    :return: str: Telegram token
    """
    token = config('TELEGRAM_TOKEN')

    if token.startswith('<') or not token:
        raise Exception('Invalid or missing TELEGRAM_TOKEN in the .env file')

    return token


TELEGRAM_TOKEN = telegram_token()

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


def account_id() -> str:
    """
    Cloudflare Account ID Validation
    :return: str: Account ID
    """
    a_id = config('ACCOUNT_ID')

    if a_id.startswith('<') or not a_id:
        raise Exception('Invalid or missing Cloudflare ACCOUNT_ID in the .env file')

    return a_id


def access_key() -> str:
    """
    Cloudflare Access Key Validation
    :return: str: Access Key
    """
    a_key = config('ACCESS_KEY')

    if a_key.startswith('<') or not a_key:
        raise Exception('Invalid or missing Cloudflare ACCESS_KEY in the .env file')

    return a_key


def secret_key() -> str:
    """
    Cloudflare Secret Key Validation
    :return: str: Secret Key
    """
    s_key = config('SECRET_KEY')

    if s_key.startswith('<') or not s_key:
        raise Exception('Invalid or missing Cloudflare SECRET_KEY in the .env file')

    return s_key


TELEGRAM_TOKEN = telegram_token()
ACCOUNT_ID     = account_id()
ACCESS_KEY     = access_key()
SECRET_KEY     = secret_key()

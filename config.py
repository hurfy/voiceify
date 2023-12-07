from decouple import config


# Telegram -------------------------------------------------------------------------------------------------------------
def telegram_token_validation() -> str:
    """
    Telegram Token Validation
    :return: str: Telegram token
    """
    token = config('TELEGRAM_TOKEN')

    if token.startswith('<') or not token:
        raise Exception('Invalid or missing TELEGRAM_TOKEN in the .env file')

    return token


# Cloudflare -----------------------------------------------------------------------------------------------------------
def account_id_validation() -> str:
    """
    Cloudflare S3 Account ID Validation
    :return: str: Cloudflare S3 Account ID
    """
    account_id = config('ACCOUNT_ID')

    if account_id.startswith('<') or not account_id:
        raise Exception('Invalid or missing ACCOUNT_ID in the .env file')

    return account_id


def access_key_validation() -> str:
    """
    Cloudflare S3 Access Key Validation
    :return: str: Cloudflare S3 Access Key
    """
    access_key = config('ACCESS_KEY')

    if access_key.startswith('<') or not access_key:
        raise Exception('Invalid or missing ACCESS_KEY in the .env file')

    return access_key


def secret_key_validation() -> str:
    """
    Cloudflare S3 Secret Key Validation
    :return: str: Cloudflare S3 Secret Key
    """
    secret_key = config('SECRET_KEY')

    if secret_key.startswith('<') or not secret_key:
        raise Exception('Invalid or missing SECRET_KEY in the .env file')

    return secret_key


# Variables ------------------------------------------------------------------------------------------------------------
TELEGRAM_TOKEN = telegram_token_validation()
ACCOUNT_ID     = account_id_validation()
ACCESS_KEY     = access_key_validation()
SECRET_KEY     = secret_key_validation()
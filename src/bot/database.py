from sqlite3 import connect
from os.path import join, dirname


class VoiceifyDatabase:
    _DATABASE  = join(dirname(__file__), '..', 'data', 'voiceify.db')
    _instance = None

    def __new__(cls, *args, **kwargs) -> object:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def __str__(self) -> str:
        return (f'Path: {self._DATABASE}\n'
                f'Name: voiceify.db')

    def insert_user_info(self, user_id: int, user_name: str, is_premium: bool, urls: list):
        urls = '\n'.join(urls) if urls else ''

        with connect(self._DATABASE) as db:
            cursor = db.cursor()

            cursor.execute(
                'INSERT INTO users (user_id, user_name, is_premium, urls) VALUES (?, ?, ?, ?)',
                (user_id, user_name, is_premium, urls)
            )

            db.commit()


x = VoiceifyDatabase()
x.insert_user_info(123, 'thehurfy', True, [])
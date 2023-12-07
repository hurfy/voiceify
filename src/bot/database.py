from sqlite3 import connect
from os.path import join, dirname


class VoiceifyDatabase:
    _DATABASE  = join(dirname(__file__), '..', 'data', 'voiceify.db')
    _instance  = None

    def __new__(cls, *args, **kwargs) -> object:
        """
        Singleton Class
        :param args:     *args
        :param kwargs:   *kwargs
        :return: object: _instance
        """
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        """
        Init Database connect
        :return: None
        """
        with connect(self._DATABASE) as self.db:
            self.cursor = self.db.cursor()

    def __str__(self) -> str:
        """
        About Database (Path, Name)
        :return: str: Info
        """
        return (f'Path: {self._DATABASE}\n'
                f'Name: voiceify.db')

    def find_user(self, user_id: int) -> tuple:
        """
        Search for a user in the database by Telegram User ID
        :param user_id: int: Telegram User ID
        :return:      tuple: A tuple with search results
        """
        user = self.cursor.execute(
            'SELECT user_id from users WHERE user_id = (?)',
            (str(user_id),)
        ).fetchone()

        return user

    def find_user_info(self, user_id: int) -> dict or None:
        """
        Search for a user info in the database by Telegram User ID
        :param user_id: int: Telegram User ID
        :return:      tuple: A dictionary with search results | None
        """
        keys = ['id', 'user_id', 'user_name', 'is_premium', 'files']
        user = self.cursor.execute(
            'SELECT * from users WHERE user_id = (?)',
            (str(user_id),)
        ).fetchone()

        return dict(zip(keys, list(user)[:-1] + [list(user)[-1].split(';')])) if user else None

    def insert_user_info(self, user_id: int, user_name: str) -> None:
        """
        This method will be executed after the /start command if the user is in the DB
        :param user_id:   int: Telegram User ID
        :param user_name: str: Telegram Username
        :return:               None
        """
        if not self.find_user(user_id):
            self.cursor.execute(
                'INSERT INTO users (user_id, user_name, is_premium, urls) VALUES (?, ?, ?, ?)',
                (user_id, user_name, False, '')
            )

            self.db.commit()


from pprint import pprint

x = VoiceifyDatabase()
pprint(x.find_user_info(1234))
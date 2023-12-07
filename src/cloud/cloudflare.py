from config          import ACCOUNT_ID, ACCESS_KEY, SECRET_KEY
from boto3           import client
from botocore.client import Config


class CloudflareBucket:
    _instance   = None
    _account_id = ACCOUNT_ID
    _access_key = ACCESS_KEY
    _secret_key = SECRET_KEY
    _endpoint   = f'https://{_account_id}.r2.cloudflarestorage.com'

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
        Init S3 client
        :return: None
        """
        self.s3 = client(
            service_name='s3',
            endpoint_url=self._endpoint,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
            config=Config(signature_version='s3v4')
        )

    def __str__(self) -> str:
        """
        About S3 Client (Account ID, Access Key, Secret Key, Endpoint)
        :return: str: Info
        """
        return (f'Account ID: {self._account_id}\n'
                f'Access Key: {self._access_key}\n'
                f'Secret Key: {self._secret_key}\n'
                f'Endpoint  : {self._endpoint}')

    def __generate_link(self, file_name: str) -> str:
        """
        Generates a perpetual link to the file
        :param file_name: str: File name for url generating
        :return:          str: File url
        """
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'voiceify', 'Key': file_name},
            ExpiresIn=None
        )

        return url

    def get_file_list(self) -> list:
        """
        Getting a list of files and information about them
        :return: list: File list
        """
        return self.s3.list_objects_v2(Bucket='voiceify')['Contents']

    def upload_file(self, file_path: str, file_name: str) -> str:
        """
        Uploading a file to the S3 Bucket
        :param file_path: str: File path on the server
        :param file_name: str: The name that will be assigned to the file in the bucket
        :return:          str: File url
        """
        with open(file_path, 'rb') as file:
            self.s3.upload_fileobj(file, 'voiceify', f'{file_name}.ogg')

        return self.__generate_link(f'{file_name}.ogg')

    def delete_file(self, file_name: str) -> None:
        """
        Deleting a file from the S3 Bucket
        :param file_name: str: File name in the batch
        :return:               None
        """
        self.s3.delete_object(Bucket='voiceify', Key=file_name)

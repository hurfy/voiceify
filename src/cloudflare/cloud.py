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
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        self.s3 = client(
            service_name='s3',
            endpoint_url=self._endpoint,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
            config=Config(signature_version='s3v4')
        )

    def __str__(self) -> str:
        return (f'Account ID: {self._account_id}\n'
                f'Access Key: {self._access_key}\n'
                f'Secret Key: {self._secret_key}\n'
                f'Endpoint  : {self._endpoint}')

    def generate_link(self, file_name: str) -> str:
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'voiceify', 'Key': file_name},
            ExpiresIn=3600
        )

        return url

    def upload_file(self, file_path: str, file_name: str) -> None:
        with open(file_path, 'rb') as file:
            self.s3.upload_fileobj(file, 'voiceify', f'{file_name}.ogg')

    def delete_file(self, file_name: str) -> None:
        self.s3.delete_object(Bucket='voiceify', Key=file_name)



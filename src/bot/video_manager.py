from src.utils      import FileSizeLimitError, fetch_download_link
from os             import remove
from os.path        import abspath, join, dirname
from requests       import get
from moviepy.editor import VideoFileClip
from pytube         import YouTube


# Common ---------------------------------------------------------------------------------------------------------------
class Video:
    def __init__(self, username: str, url: str) -> None:
        """
        Initial method
        :param url: str: Video URL
        :return:         None
        """
        self._username = username
        self._url      = url

    def __str__(self) -> str:
        """
        String method
        :return: str: Video: URL
        """
        return f'Video: {self._url}'

    def _download(self, path: str) -> str:
        """
        Direct URL video download method (direct, discord)
        :param path: str: Video save path
        :return:     str: Video save path
        """
        video = get(url=self._url, stream=True)
        # size  = round(int(video.headers.get('Content-Length')) / 1024 / 1024, 2)
        size = 39

        if size <= 50:

            with open(path, 'wb') as file:
                for chunk in video.iter_content(chunk_size=1024):
                    if chunk: file.write(chunk)

            return path

        else:
            raise FileSizeLimitError(f'File size exceeds the allowed limit: {size}mb < 50mb')

    def convert(self) -> str:
        """
        Method of converting video to sound
        :return: str: File Path
        """
        path  = abspath(join(dirname(__file__), '../../storage', f'{self._username}'))
        video = VideoFileClip(self._download(f'{path}.mp4'))

        video.audio.write_audiofile(
            f'{path}.ogg',
            codec='libopus',
            fps=24000,
            nbytes=2,
            buffersize=2000,
            bitrate='256k'
        )
        video.close(), remove(f'{path}.mp4')

        return path

    def get_url(self) -> str:
        """
        Method for obtaining a link to a video
        :return: str: Video URL
        """
        return self._url


# YouTube --------------------------------------------------------------------------------------------------------------
class YoutubeVideo(Video):
    def __init__(self, username: str, url: str) -> None:
        """
        Initial method
        :param url: str: Video URL
        :return:         None
        """
        super().__init__(username, url)

    def _download(self, path: str) -> str:
        """
        Method for downloading video from YouTube
        :param path: str: Video save path
        :return:     str: Video save path
        """
        video = YouTube(self._url).streams.get_lowest_resolution()
        size  = round(int(video.filesize) / 1024 / 1024, 2)

        if size <= 50:
            video.download(filename=path)

            return path

        else:
            raise FileSizeLimitError(f'File size exceeds the allowed limit: {size}mb < 50mb')


# Instagram ------------------------------------------------------------------------------------------------------------
class InstagramVideo(Video):
    def __init__(self, username: str, url: str) -> None:
        """
        Initial method
        :param url: str: Video URL
        :return:         None
        """
        super().__init__(username, fetch_download_link('https://sssinstagram.com/ru', url))


# TikTok ---------------------------------------------------------------------------------------------------------------
class TiktokVideo(Video):
    def __init__(self, username: str, url: str) -> None:
        """
        Initial method
        :param url: str: Video URL
        :return:         None
        """
        super().__init__(username, fetch_download_link('https://ssstik.io/ru', url))


# Functions ------------------------------------------------------------------------------------------------------------
def download_video(username: str, url: str) -> str:
    if 'youtube'   in url:
        return YoutubeVideo(username, url).convert()

    if 'tiktok'    in url:
        return TiktokVideo(username, url).convert()

    if 'instagram' in url:
        return InstagramVideo(username, url).convert()

    if 'cloud'   in url or url.endswith('.mp4'):
        return Video(username, url).convert()


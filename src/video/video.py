from requests       import get
from moviepy.editor import VideoFileClip
from os             import remove


class Video:
    def __init__(self, url: str) -> None:
        """
        Initial method
        :param url: str: Video URL
        :return:         None
        """
        self.__url   = url
        self.__video = self.download(fr'test.mp4')

    def __str__(self) -> str:
        """
        String method
        :return: str: Video: URL
        """
        return f'Video: {self.__url}'

    def get_url(self) -> str:
        """
        Method for obtaining a link to a video
        :return: str: Video URL
        """
        return self.__url

    def get_video(self) -> str:
        """
        Method for obtaining the path to the video file
        :return: str: Video path
        """
        return self.__video

    def download(self, path: str) -> str:
        """
        Direct URL video download method (direct, discord)
        :param path: str: Video save path
        :return:     str: Video save path
        """
        video = get(url=self.__url, stream=True)

        with open(path, 'wb') as file:
            for chunk in video.iter_content(chunk_size=1024):
                if chunk: file.write(chunk)

        return path

    def convert(self) -> None:
        """
        Method of converting video to sound
        :return: None
        """
        VideoFileClip(self.__video).audio.write_audiofile('test.mp3')
        remove(self.__video)

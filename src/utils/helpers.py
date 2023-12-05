from os                            import remove
from selenium                      import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions
from selenium.webdriver.common.by  import By

ERRORS = [
       'Huh?🤨',
       'Try writing /start😏',
       'It\'s beautiful weather outside!🌤',
       '404: Wit not found. Try upgrading to Wit 2.0🧠',
       'I\'m fluent in emoji, but your message seems to be written in hieroglyphics. Any translation services '
       'available?🤓',
       'Error 418: I\'m a teapot. Your message is too hot to handle!🍵',
       'Command not recognized. Did you mean to summon a unicorn?🦄',
       'This message is brought to you by the Department of Unintelligible Communications. Can you please speak in '
       'human?👽',
       'Message decryption failed. Are you sure you\'re not a spy from the Secret Society of Puzzling Punctuation?🤪',
       'Error 007: Message too spy-like. Are you James Bond in disguise?🕵️'
]


class FileSizeLimitError(Exception):
    def __init__(self, message: str) -> None:
        """
        Initial method
        :param message: str: Error message
        :return:             None
        """
        self.message = message
        super().__init__(self.message)


def create_driver(url: str) -> webdriver:
    """
    The function creates a selenium webdriver and loads a web page in the current browser session
    :param url:    str: Page URL
    :return: webdriver: Driver object
    """
    options = webdriver.ChromeOptions()
    options_list = [
        '--headless',
        '--window-size=1920,1080',
        '--enable-javascript',
        '--user-agent=\'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0\''
    ]

    for option in options_list:
        options.add_argument(option)

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver


def fetch_download_link(site_url: str, video_url: str) -> str:
    """
    The function creates a session with a website to download a video, finds and returns a direct link to the video
    :param site_url:  str: Site URL
    :param video_url: str: Video URL
    :return:          str: Video download URL
    """
    driver = create_driver(site_url)

    input_element = driver.find_element(by=By.ID, value='main_page_text')
    input_element.send_keys(video_url)

    button_name     = 'without_watermark' if 'tik' in site_url else 'download-btn'
    download_button = driver.find_element(by=By.ID, value='submit')
    download_button.click()

    return WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located
                                           ((By.CLASS_NAME, button_name))).get_attribute('href')


def delete_file(file_name: str) -> None:
    remove(file_name)

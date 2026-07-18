import webbrowser
import urllib.parse
from system.window_manager import WindowManager



class BrowserAutomation:


    def __init__(self):

        self.window = WindowManager()



    def open_chrome(self):

        webbrowser.open(
            "https://www.google.com"
        )



    def open_youtube(self, query):

        url = "https://www.youtube.com/results?search_query="

        search = urllib.parse.quote(query)

        webbrowser.open(
            url + search
        )



    def open_google(self, query):

        url = "https://www.google.com/search?q="

        search = urllib.parse.quote(query)

        webbrowser.open(
            url + search
        )



    def close_youtube(self):

        if self.window.is_youtube_open():

            closed = self.window.close_youtube_window()


            if closed:

                return True


        return False

import pygetwindow as gw
import psutil


class WindowManager:


    def get_active_window(self):

        try:

            window = gw.getActiveWindow()

            if window:

                return window.title

            return None

        except Exception:

            return None



    def get_all_windows(self):

        try:

            return gw.getAllTitles()

        except Exception:

            return []



    def is_browser_open(self):

        browsers = [
            "msedge.exe",
            "chrome.exe"
        ]


        for process in psutil.process_iter(
            ["name"]
        ):

            try:

                if process.info["name"]:

                    if process.info["name"].lower() in browsers:

                        return True


            except Exception:

                pass


        return False



    def is_youtube_open(self):

        # First check title

        windows = self.get_all_windows()


        for title in windows:

            if title:

                title = title.lower()


                if "youtube" in title:

                    return True



        # Browser running check

        if self.is_browser_open():

            return True



        return False



    def close_youtube_window(self):

        windows = gw.getAllWindows()


        for window in windows:

            try:

                title = window.title.lower()


                if (
                    "youtube" in title
                    or
                    "microsoft edge" in title
                    or
                    "google chrome" in title
                ):

                    window.close()

                    return True


            except Exception:

                pass


        return False
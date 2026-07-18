import time
import pygetwindow as gw


class WindowService:

    def get_all_windows(self):

        windows = []

        for window in gw.getAllWindows():

            try:

                if window.title.strip():

                    windows.append(window)

            except Exception:

                pass

        return windows



    def find(self, target):

        target = target.lower()


        for window in self.get_all_windows():

            try:

                if target in window.title.lower():

                    return window

            except Exception:

                pass


        return None



    def activate(self, target):

        window = self.find(target)


        if window is None:

            return False


        try:

            if window.isMinimized:

                window.restore()

                time.sleep(0.2)


            window.activate()

            time.sleep(0.3)

            return True


        except Exception:

            return False



    def close(self, target):

        window = self.find(target)


        if window is None:

            return False


        try:

            window.close()

            return True


        except Exception:

            return False



    def minimize(self, target):

        window = self.find(target)


        if window is None:

            return False


        try:

            window.minimize()

            return True


        except Exception:

            return False



    def maximize(self, target):

        window = self.find(target)


        if window is None:

            return False


        try:

            window.maximize()

            return True


        except Exception:

            return False



    def title(self):

        try:

            window = gw.getActiveWindow()

            if window:

                return window.title

        except Exception:

            pass


        return None

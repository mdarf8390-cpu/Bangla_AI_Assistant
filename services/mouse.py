import pyautogui
import logging

logger = logging.getLogger(__name__)


class MouseService:

    def move(self, x, y, duration=0.2):
        
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"Coordinates must be numbers, got x={type(x).__name__}, y={type(y).__name__}")
            return False
        
        if duration < 0:
            logger.error(f"Duration must be non-negative, got {duration}")
            return False
        
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            logger.error(f"Failed to move mouse to ({x}, {y}): {str(e)}")
            return False


    def click(self, x=None, y=None):

        try:
            if x is not None and y is not None:
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    logger.error(f"Coordinates must be numbers")
                    return False
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return True
        except Exception as e:
            logger.error(f"Failed to click at ({x}, {y}): {str(e)}")
            return False


    def double_click(self, x=None, y=None):

        try:
            if x is not None and y is not None:
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    logger.error(f"Coordinates must be numbers")
                    return False
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.doubleClick()
            return True
        except Exception as e:
            logger.error(f"Failed to double click at ({x}, {y}): {str(e)}")
            return False


    def right_click(self, x=None, y=None):

        try:
            if x is not None and y is not None:
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    logger.error(f"Coordinates must be numbers")
                    return False
                pyautogui.rightClick(x, y)
            else:
                pyautogui.rightClick()
            return True
        except Exception as e:
            logger.error(f"Failed to right click at ({x}, {y}): {str(e)}")
            return False


    def drag(self, x, y, duration=0.3):

        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"Coordinates must be numbers")
            return False
        
        if duration < 0:
            logger.error(f"Duration must be non-negative")
            return False

        try:
            pyautogui.dragTo(
                x,
                y,
                duration=duration
            )
            return True
        except Exception as e:
            logger.error(f"Failed to drag to ({x}, {y}): {str(e)}")
            return False


    def scroll(self, amount):

        if not isinstance(amount, int):
            logger.error(f"Scroll amount must be integer, got {type(amount).__name__}")
            return False

        try:
            pyautogui.scroll(amount)
            return True
        except Exception as e:
            logger.error(f"Failed to scroll by {amount}: {str(e)}")
            return False


    def position(self):

        try:
            return pyautogui.position()
        except Exception as e:
            logger.error(f"Failed to get mouse position: {str(e)}")
            return None

import re
import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class CommandType(Enum):
    """Types of commands"""
    CREATE_FILE = "create_file"
    WRITE_FILE = "write_file"
    READ_FILE = "read_file"
    DELETE_FILE = "delete_file"
    DELETE_DIR = "delete_dir"
    LIST_FILES = "list_files"
    COPY_FILE = "copy_file"
    RENAME_FILE = "rename_file"
    CREATE_DIR = "create_dir"
    FILE_INFO = "file_info"
    OPEN_FILE = "open_file"
    TYPE_TEXT = "type_text"
    MOUSE_MOVE = "mouse_move"
    MOUSE_CLICK = "mouse_click"
    KEYBOARD_PRESS = "keyboard_press"
    CLIPBOARD_COPY = "clipboard_copy"
    CLIPBOARD_PASTE = "clipboard_paste"
    UNKNOWN = "unknown"


class CommandParser:
    """Parse natural language Bangla commands"""
    
    def __init__(self):
        self.command_patterns = {
            # File creation patterns
            CommandType.CREATE_FILE: [
                r"(তৈরি করো|বানাও|নতুন) (?:একটা|একটি)? (?:ফাইল|file) (?:নাম|named)? ['\"]?([^'\"]+)['\"]?",
                r"([^'\"]+) নাম (?:একটা|একটি)? (?:ফাইল|file) (?:তৈরি করো|বানাও)",
                r"(?:ফাইল|file) (?:তৈরি করো|বানাও) ([^'\"]+) (?:এ|তে)?",
            ],
            
            # File writing patterns
            CommandType.WRITE_FILE: [
                r"(এ|তে) ['\"]?([^'\"]+)['\"]? (?:লিখ|লেখ|type করো|write করো)",
                r"([^'\"]+) (?:লিখ|লেখ|type করো|write করো) ([^ ]+) (?:এ|তে)",
                r"(?:এখানে|এতে) ['\"]?([^'\"]+)['\"]? (?:লিখ|লেখ|add করো|যোগ করো)",
            ],
            
            # File reading patterns
            CommandType.READ_FILE: [
                r"(?:পড়|পড়ো|read করো|দেখ|দেখাও) ([^ ]+) (?:ফাইল|file)?",
                r"([^ ]+) (?:ফাইল|file)? (?:এর|এর) (?:কন্টেন্ট|বিষয়বস্তু) (?:পড়|পড়ো|read করো|দেখ|দেখাও)",
            ],
            
            # File deletion patterns
            CommandType.DELETE_FILE: [
                r"(?:delete|ডিলিট) করো ([^ ]+) (?:ফাইল|file)?",
                r"([^ ]+) (?:ফাইল|file)? (?:delete|ডিলিট) করো",
                r"(?:delete|ডিলিট) করো ([^ ]+)",
            ],
            
            # Directory deletion patterns
            CommandType.DELETE_DIR: [
                r"(?:delete|ডিলিট) করো ([^ ]+) (?:directory|ডিরেক্টরি|folder|ফোল্ডার)",
                r"([^ ]+) (?:directory|ডিরেক্টরি|folder|ফোল্ডার) (?:delete|ডিলিট) করো",
            ],
            
            # List files patterns
            CommandType.LIST_FILES: [
                r"(?:দেখ|দেখাও|list|তালিকা) ([^ ]+) (?:এর|এর) (?:ফাইল|file|contents)",
                r"([^ ]+) (?:এ|তে) (?:কি কি|কি|কোন কোন) (?:ফাইল|file) (?:আছে|আছে)?",
                r"(?:সব|all) (?:ফাইল|file) (?:দেখ|দেখাও|list|তালিকা) ([^ ]+) (?:এ|তে)?",
            ],
            
            # File copy patterns
            CommandType.COPY_FILE: [
                r"([^ ]+) copy করো ([^ ]+) (এ|তে)",
                r"([^ ]+) (?:ফাইল|file) copy করো ([^ ]+) (এ|তে)",
                r"copy করো ([^ ]+) থেকে ([^ ]+) (এ|তে)",
            ],
            
            # File rename patterns
            CommandType.RENAME_FILE: [
                r"rename করো ([^ ]+) নতুন নাম ([^ ]+)",
                r"([^ ]+) (?:ফাইল|file)? rename করো ([^ ]+)",
                r"([^ ]+) এর নাম বদল করো ([^ ]+)",
            ],
            
            # Directory creation patterns
            CommandType.CREATE_DIR: [
                r"(?:directory|ডিরেক্টরি|folder|ফোল্ডার) (?:তৈরি করো|বানাও) ([^ ]+)",
                r"([^ ]+) (?:directory|ডিরেক্টরি|folder|ফোল্ডার) (?:তৈরি করো|বানাও)",
            ],
            
            # File info patterns
            CommandType.FILE_INFO: [
                r"(?:তথ্য|info|information) ([^ ]+) (?:ফাইল|file)?",
                r"([^ ]+) (?:ফাইল|file)? (?:এর|এর) (?:তথ্য|info|information) (?:দেখ|দেখাও)?",
            ],
            
            # Type text patterns
            CommandType.TYPE_TEXT: [
                r"(?:type|টাইপ) করো ['\"]?([^'\"]+)['\"]?",
                r"['\"]?([^'\"]+)['\"]? (?:type|টাইপ) করো",
                r"(?:এই|এই) ['\"]?([^'\"]+)['\"]? (?:type|টাইপ|লিখ|লেখ)",
            ],
            
            # Mouse move patterns
            CommandType.MOUSE_MOVE: [
                r"mouse move করো ([0-9]+) ([0-9]+) (এ|তে)",
                r"mouse ([0-9]+)[,\s]([0-9]+) (এ|তে) move করো",
            ],
            
            # Mouse click patterns
            CommandType.MOUSE_CLICK: [
                r"mouse click করো ([0-9]+) ([0-9]+) (এ|তে)",
                r"([0-9]+)[,\s]([0-9]+) (এ|তে) click করো",
            ],
            
            # Keyboard press patterns
            CommandType.KEYBOARD_PRESS: [
                r"(?:key|কী) press করো ([^ ]+)",
                r"([^ ]+) key press করো",
                r"([^ ]+) (?:চাপ|press) করো",
            ],
            
            # Clipboard copy patterns
            CommandType.CLIPBOARD_COPY: [
                r"copy করো ['\"]?([^'\"]+)['\"]?",
                r"['\"]?([^'\"]+)['\"]? copy করো",
                r"(?:clipboard|ক্লিপবোর্ড) (এ|তে) copy করো ['\"]?([^'\"]+)['\"]?",
            ],
            
            # Clipboard paste patterns
            CommandType.CLIPBOARD_PASTE: [
                r"paste করো",
                r"(?:clipboard|ক্লিপবোর্ড) থেকে paste করো",
            ],
        }
    
    def parse(self, command_text: str) -> Tuple[CommandType, Dict[str, any]]:
        """Parse natural language command"""
        try:
            command_text = command_text.strip().lower()
            
            # Try to match each command type
            for cmd_type, patterns in self.command_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, command_text, re.IGNORECASE)
                    if match:
                        params = self._extract_parameters(cmd_type, match, command_text)
                        logger.info(f"Parsed command: {cmd_type.value} with params: {params}")
                        return cmd_type, params
            
            logger.warning(f"Could not parse command: {command_text}")
            return CommandType.UNKNOWN, {"original": command_text}
        
        except Exception as e:
            logger.error(f"Error parsing command: {str(e)}")
            return CommandType.UNKNOWN, {"error": str(e)}
    
    def _extract_parameters(self, cmd_type: CommandType, match, original_text: str) -> Dict:
        """Extract parameters from regex match"""
        params = {}
        
        if cmd_type == CommandType.CREATE_FILE:
            params["file_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.WRITE_FILE:
            groups = match.groups()
            params["file_path"] = groups[0]
            params["content"] = groups[1] if len(groups) > 1 else ""
        
        elif cmd_type == CommandType.READ_FILE:
            params["file_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.DELETE_FILE:
            params["file_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.DELETE_DIR:
            params["dir_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.LIST_FILES:
            params["directory"] = match.group(match.lastindex) or "desktop"
        
        elif cmd_type == CommandType.COPY_FILE:
            groups = match.groups()
            params["source"] = groups[0]
            params["destination"] = groups[1]
        
        elif cmd_type == CommandType.RENAME_FILE:
            groups = match.groups()
            params["old_name"] = groups[0]
            params["new_name"] = groups[1]
        
        elif cmd_type == CommandType.CREATE_DIR:
            params["dir_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.FILE_INFO:
            params["file_path"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.TYPE_TEXT:
            params["text"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.MOUSE_MOVE:
            groups = match.groups()
            params["x"] = int(groups[0])
            params["y"] = int(groups[1])
        
        elif cmd_type == CommandType.MOUSE_CLICK:
            groups = match.groups()
            params["x"] = int(groups[0])
            params["y"] = int(groups[1])
        
        elif cmd_type == CommandType.KEYBOARD_PRESS:
            params["key"] = match.group(match.lastindex)
        
        elif cmd_type == CommandType.CLIPBOARD_COPY:
            params["text"] = match.group(match.lastindex)
        
        return params
    
    def suggest_command(self, partial_text: str) -> List[str]:
        """Suggest possible commands based on partial text"""
        suggestions = []
        partial_lower = partial_text.lower()
        
        for cmd_type in CommandType:
            if cmd_type != CommandType.UNKNOWN:
                if partial_lower in cmd_type.value:
                    suggestions.append(cmd_type.value)
        
        return suggestions


class CommandExecutor:
    """Execute parsed commands"""
    
    def __init__(self, file_manager=None, keyboard_handler=None, mouse_handler=None, clipboard_handler=None):
        self.file_manager = file_manager
        self.keyboard_handler = keyboard_handler
        self.mouse_handler = mouse_handler
        self.clipboard_handler = clipboard_handler
        self.parser = CommandParser()
    
    def execute(self, command_text: str) -> Tuple[bool, str]:
        """Execute a natural language command"""
        try:
            cmd_type, params = self.parser.parse(command_text)
            
            if cmd_type == CommandType.CREATE_FILE:
                return self._handle_create_file(params)
            
            elif cmd_type == CommandType.WRITE_FILE:
                return self._handle_write_file(params)
            
            elif cmd_type == CommandType.READ_FILE:
                return self._handle_read_file(params)
            
            elif cmd_type == CommandType.DELETE_FILE:
                return self._handle_delete_file(params)
            
            elif cmd_type == CommandType.DELETE_DIR:
                return self._handle_delete_dir(params)
            
            elif cmd_type == CommandType.LIST_FILES:
                return self._handle_list_files(params)
            
            elif cmd_type == CommandType.COPY_FILE:
                return self._handle_copy_file(params)
            
            elif cmd_type == CommandType.RENAME_FILE:
                return self._handle_rename_file(params)
            
            elif cmd_type == CommandType.CREATE_DIR:
                return self._handle_create_dir(params)
            
            elif cmd_type == CommandType.FILE_INFO:
                return self._handle_file_info(params)
            
            elif cmd_type == CommandType.TYPE_TEXT:
                return self._handle_type_text(params)
            
            elif cmd_type == CommandType.MOUSE_MOVE:
                return self._handle_mouse_move(params)
            
            elif cmd_type == CommandType.MOUSE_CLICK:
                return self._handle_mouse_click(params)
            
            elif cmd_type == CommandType.KEYBOARD_PRESS:
                return self._handle_keyboard_press(params)
            
            elif cmd_type == CommandType.CLIPBOARD_COPY:
                return self._handle_clipboard_copy(params)
            
            elif cmd_type == CommandType.CLIPBOARD_PASTE:
                return self._handle_clipboard_paste(params)
            
            else:
                return False, "❌ Command বুঝতে পারলাম না। আরও স্পষ্ট করে বলুন।"
        
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def _handle_create_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.create_file(params.get("file_path", ""), "")
    
    def _handle_write_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.write_to_file(
            params.get("file_path", ""),
            params.get("content", "")
        )
    
    def _handle_read_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.read_file(params.get("file_path", ""))
    
    def _handle_delete_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.delete_file(params.get("file_path", ""))
    
    def _handle_delete_dir(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.delete_directory(params.get("dir_path", ""))
    
    def _handle_list_files(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.list_files(params.get("directory", "desktop"))
    
    def _handle_copy_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.copy_file(
            params.get("source", ""),
            params.get("destination", "")
        )
    
    def _handle_rename_file(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.rename_file(
            params.get("old_name", ""),
            params.get("new_name", "")
        )
    
    def _handle_create_dir(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.create_directory(params.get("dir_path", ""))
    
    def _handle_file_info(self, params: Dict) -> Tuple[bool, str]:
        if not self.file_manager:
            return False, "❌ File manager available নেই"
        return self.file_manager.get_file_info(params.get("file_path", ""))
    
    def _handle_type_text(self, params: Dict) -> Tuple[bool, str]:
        if not self.keyboard_handler:
            return False, "❌ Keyboard handler available নেই"
        try:
            self.keyboard_handler.type_text(params.get("text", ""))
            return True, f"✅ '{params.get('text', '')}' type হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def _handle_mouse_move(self, params: Dict) -> Tuple[bool, str]:
        if not self.mouse_handler:
            return False, "❌ Mouse handler available নেই"
        try:
            x = params.get("x", 0)
            y = params.get("y", 0)
            self.mouse_handler.move(x, y)
            return True, f"✅ Mouse ({x}, {y}) এ move হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def _handle_mouse_click(self, params: Dict) -> Tuple[bool, str]:
        if not self.mouse_handler:
            return False, "❌ Mouse handler available নেই"
        try:
            x = params.get("x", 0)
            y = params.get("y", 0)
            self.mouse_handler.click(x, y)
            return True, f"✅ ({x}, {y}) এ click হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def _handle_keyboard_press(self, params: Dict) -> Tuple[bool, str]:
        if not self.keyboard_handler:
            return False, "❌ Keyboard handler available নেই"
        try:
            key = params.get("key", "")
            self.keyboard_handler.press(key)
            return True, f"✅ '{key}' key press হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def _handle_clipboard_copy(self, params: Dict) -> Tuple[bool, str]:
        if not self.clipboard_handler:
            return False, "❌ Clipboard handler available নেই"
        try:
            text = params.get("text", "")
            self.clipboard_handler.copy(text)
            return True, f"✅ Clipboard এ copy হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def _handle_clipboard_paste(self, params: Dict) -> Tuple[bool, str]:
        if not self.clipboard_handler:
            return False, "❌ Clipboard handler available নেই"
        try:
            self.clipboard_handler.paste()
            return True, "✅ Clipboard থেকে paste হয়েছে"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"


# Global instances
command_parser = None
command_executor = None


def initialize_command_system(file_manager=None, keyboard=None, mouse=None, clipboard=None):
    """Initialize command system"""
    global command_parser, command_executor
    command_parser = CommandParser()
    command_executor = CommandExecutor(file_manager, keyboard, mouse, clipboard)
    return command_parser, command_executor


def get_command_executor() -> CommandExecutor:
    """Get global command executor"""
    global command_executor
    if command_executor is None:
        command_executor = CommandExecutor()
    return command_executor


def get_command_parser() -> CommandParser:
    """Get global command parser"""
    global command_parser
    if command_parser is None:
        command_parser = CommandParser()
    return command_parser

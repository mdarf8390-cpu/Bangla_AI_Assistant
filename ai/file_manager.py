import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class FileManager:
    """Manage file operations with smart path handling"""
    
    def __init__(self):
        self.home_dir = str(Path.home())
        self.desktop_dir = os.path.join(self.home_dir, "Desktop")
        self.documents_dir = os.path.join(self.home_dir, "Documents")
        self.downloads_dir = os.path.join(self.home_dir, "Downloads")
        
        # Ensure directories exist
        self._ensure_directory(self.desktop_dir)
        self._ensure_directory(self.documents_dir)
        self._ensure_directory(self.downloads_dir)
    
    def _ensure_directory(self, path: str) -> bool:
        """Ensure directory exists"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            return True
        except Exception as e:
            logger.error(f"Error ensuring directory {path}: {str(e)}")
            return False
    
    def _resolve_path(self, file_path: str) -> Optional[str]:
        """Resolve file path intelligently"""
        try:
            # If it's an absolute path
            if os.path.isabs(file_path):
                return file_path
            
            # If it mentions Desktop
            if "desktop" in file_path.lower():
                filename = file_path.lower().replace("desktop", "").strip()
                return os.path.join(self.desktop_dir, filename)
            
            # If it mentions Documents
            if "documents" in file_path.lower() or "document" in file_path.lower():
                filename = file_path.lower().replace("documents", "").replace("document", "").strip()
                return os.path.join(self.documents_dir, filename)
            
            # If it mentions Downloads
            if "downloads" in file_path.lower() or "download" in file_path.lower():
                filename = file_path.lower().replace("downloads", "").replace("download", "").strip()
                return os.path.join(self.downloads_dir, filename)
            
            # Default to Desktop
            return os.path.join(self.desktop_dir, file_path)
        
        except Exception as e:
            logger.error(f"Error resolving path {file_path}: {str(e)}")
            return None
    
    def create_file(self, file_path: str, content: str = "") -> tuple:
        """Create a new file"""
        try:
            resolved_path = self._resolve_path(file_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            # Create parent directories if needed
            parent_dir = os.path.dirname(resolved_path)
            self._ensure_directory(parent_dir)
            
            # Create file
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"File created: {resolved_path}")
            return True, f"✅ File তৈরি হয়েছে: {os.path.basename(resolved_path)}"
        
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def write_to_file(self, file_path: str, content: str, append: bool = False) -> tuple:
        """Write content to file"""
        try:
            resolved_path = self._resolve_path(file_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(resolved_path):
                return self.create_file(file_path, content)
            
            mode = 'a' if append else 'w'
            with open(resolved_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Content written to: {resolved_path}")
            action = "যোগ করা" if append else "লেখা"
            return True, f"✅ Content {action} হয়েছে"
        
        except Exception as e:
            logger.error(f"Error writing to file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def read_file(self, file_path: str) -> tuple:
        """Read file content"""
        try:
            resolved_path = self._resolve_path(file_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(resolved_path):
                return False, f"❌ File পাওয়া যায়নি: {file_path}"
            
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"File read: {resolved_path}")
            return True, content
        
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def delete_file(self, file_path: str) -> tuple:
        """Delete a file"""
        try:
            resolved_path = self._resolve_path(file_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(resolved_path):
                return False, f"❌ File পাওয়া যায়নি: {file_path}"
            
            if os.path.isdir(resolved_path):
                return False, "❌ এটি একটি directory, file নয়"
            
            os.remove(resolved_path)
            logger.info(f"File deleted: {resolved_path}")
            return True, f"✅ {os.path.basename(resolved_path)} delete হয়েছে"
        
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def delete_directory(self, dir_path: str) -> tuple:
        """Delete a directory"""
        try:
            resolved_path = self._resolve_path(dir_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(resolved_path):
                return False, f"❌ Directory পাওয়া যায়নি: {dir_path}"
            
            if not os.path.isdir(resolved_path):
                return False, "❌ এটি একটি directory নয়"
            
            shutil.rmtree(resolved_path)
            logger.info(f"Directory deleted: {resolved_path}")
            return True, f"✅ {os.path.basename(resolved_path)} directory delete হয়েছে"
        
        except Exception as e:
            logger.error(f"Error deleting directory: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def list_files(self, dir_path: str = "desktop") -> tuple:
        """List files in directory"""
        try:
            # Map shorthand to full path
            if dir_path.lower() == "desktop":
                target_dir = self.desktop_dir
            elif dir_path.lower() in ["documents", "document"]:
                target_dir = self.documents_dir
            elif dir_path.lower() in ["downloads", "download"]:
                target_dir = self.downloads_dir
            else:
                target_dir = self._resolve_path(dir_path)
            
            if not target_dir or not os.path.exists(target_dir):
                return False, f"❌ Directory পাওয়া যায়নি"
            
            files = os.listdir(target_dir)
            if not files:
                return True, "📭 Directory খালি"
            
            file_list = "📋 Files:\n"
            for file in files:
                file_path = os.path.join(target_dir, file)
                if os.path.isdir(file_path):
                    file_list += f"📁 {file}/\n"
                else:
                    file_list += f"📄 {file}\n"
            
            logger.info(f"Listed files in: {target_dir}")
            return True, file_list
        
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def copy_file(self, source: str, destination: str) -> tuple:
        """Copy file"""
        try:
            source_path = self._resolve_path(source)
            dest_path = self._resolve_path(destination)
            
            if not source_path or not dest_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(source_path):
                return False, f"❌ Source file পাওয়া যায়নি"
            
            # Create parent directory if needed
            parent_dir = os.path.dirname(dest_path)
            self._ensure_directory(parent_dir)
            
            shutil.copy2(source_path, dest_path)
            logger.info(f"File copied: {source_path} -> {dest_path}")
            return True, f"✅ {os.path.basename(source)} copy হয়েছে"
        
        except Exception as e:
            logger.error(f"Error copying file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def rename_file(self, old_name: str, new_name: str) -> tuple:
        """Rename file"""
        try:
            old_path = self._resolve_path(old_name)
            
            if not old_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(old_path):
                return False, f"❌ File পাওয়া যায়নি"
            
            # Keep the same directory
            parent_dir = os.path.dirname(old_path)
            new_path = os.path.join(parent_dir, new_name)
            
            os.rename(old_path, new_path)
            logger.info(f"File renamed: {old_path} -> {new_path}")
            return True, f"✅ {os.path.basename(old_name)} rename হয়েছে {new_name}"
        
        except Exception as e:
            logger.error(f"Error renaming file: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        try:
            resolved_path = self._resolve_path(file_path)
            if resolved_path:
                return os.path.exists(resolved_path)
            return False
        except Exception as e:
            logger.error(f"Error checking file existence: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> tuple:
        """Get file information"""
        try:
            resolved_path = self._resolve_path(file_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if not os.path.exists(resolved_path):
                return False, f"❌ File পাওয়া যায়নি"
            
            stat_info = os.stat(resolved_path)
            size_kb = stat_info.st_size / 1024
            created_time = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            info = f"""📊 File Information:
📄 Name: {os.path.basename(resolved_path)}
📁 Path: {resolved_path}
💾 Size: {size_kb:.2f} KB
📅 Created: {created_time}
🕐 Modified: {modified_time}"""
            
            return True, info
        
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return False, f"❌ Error: {str(e)}"
    
    def create_directory(self, dir_path: str) -> tuple:
        """Create a new directory"""
        try:
            resolved_path = self._resolve_path(dir_path)
            if not resolved_path:
                return False, "❌ Path রিজলভ করতে পারলাম না"
            
            if os.path.exists(resolved_path):
                return False, f"❌ Directory ইতিমধ্যে আছে"
            
            os.makedirs(resolved_path)
            logger.info(f"Directory created: {resolved_path}")
            return True, f"✅ Directory তৈরি হয়েছে: {os.path.basename(resolved_path)}"
        
        except Exception as e:
            logger.error(f"Error creating directory: {str(e)}")
            return False, f"❌ Error: {str(e)}"


# Global instance
file_manager = None


def initialize_file_manager() -> FileManager:
    """Initialize global file manager"""
    global file_manager
    file_manager = FileManager()
    return file_manager


def get_file_manager() -> FileManager:
    """Get global file manager instance"""
    global file_manager
    if file_manager is None:
        file_manager = FileManager()
    return file_manager

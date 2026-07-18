# core/system_manager.py
import importlib
import os

class SystemManager:
    def __init__(self):
        self.services = {}

    def load_services(self):
        # 'services' ফোল্ডারের সবগুলোকে অটোমেটিক লোড করবে
        service_path = 'services'
        for file in os.listdir(service_path):
            if file.endswith(".py"):
                module_name = file[:-3]
                self.services[module_name] = importlib.import_module(f"services.{module_name}")
        print("System Services Loaded Successfully.")

    def get_service(self, name):
        return self.services.get(name)

# এটাকে মেইন প্রোগ্রামে কল করবেন
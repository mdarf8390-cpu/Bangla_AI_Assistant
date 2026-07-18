class SecurityManager:
    def __init__(self, master_password="mysecretpassword"):
        self.master_password = master_password
        self.pending_task = None
        self.is_waiting = False

    def request_approval(self, task_data):
        """কাজটি হোল্ড করে রাখা"""
        self.pending_task = task_data
        self.is_waiting = True
        return "⚠️ এই কাজটি করার জন্য পাসওয়ার্ড প্রয়োজন। অনুগ্রহ করে পাসওয়ার্ডটি দিন।"

    def verify(self, password):
        """পাসওয়ার্ড ভেরিফাই করা"""
        if self.is_waiting and password == self.master_password:
            task = self.pending_task
            self.reset()
            return True, task
        return False, None

    def reset(self):
        self.pending_task = None
        self.is_waiting = False

security_manager = SecurityManager(master_password="123") # এখানে আপনার গোপন পাসওয়ার্ড দিন
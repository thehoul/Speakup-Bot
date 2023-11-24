import threading

class Store:

    def __init__(self, value):
        assert value > 0, "Value must be greater than 0"
        self.val = value
        self.lock = threading.Lock()

    def get_job(self):
        with self.lock:
            if self.val > 0:
                self.val -= 1
                return True
            else:
                return False

    def get_val(self):
        return self.val
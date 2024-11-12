import getpass

class Keybad:
    def get_input(self, message, secure=False):
        def get_secure_input(message):
            return getpass.getpass(message)
        
        if secure:
            return get_secure_input(message) 
        return input(message)

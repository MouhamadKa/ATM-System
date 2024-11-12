import os

class Screen:
    def clear_screen(self):
        os.system('cls' if os.name=='nt' else 'clear')
        
    def show_message(self, message):
        print(message)
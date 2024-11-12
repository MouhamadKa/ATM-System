from authenticator import Authenticator
class CardReader:
    def __init__(self, atm):
        self.atm = atm
        self.authenticator = Authenticator(self.atm.bank)
        
    def insert_card(self, card):
        pin = self.atm.keybad.get_input('Please enter your PIN: ', secure=True)
        account =  self.authenticator.authenticate(card.number, pin)
        
        if account:
            self.atm.display_main_menu(account)
        else:
            self.atm.screen.show_message('Invalid card or PIN')
            return None
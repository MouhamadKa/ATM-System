from screen import Screen
from account import Account
from transactions import *

class WithdrawHandler:
    def __init__(self, keybad, screen:Screen):
        self.keybad = keybad
        self.screen = screen
        
    def handle(self, account):
        while True:
            try:
                amount = float(self.keybad.get_input('Enter the amout to withdraw: '))
                if amount <= 0:
                    self.screen.show_message('Invalid amount. Please Enter a positive number...')
                    continue
                transaction = WithdrawTransaction(amount)
                transaction.excute(account)
                break
            except ValueError:
                self.screen.show_message('Invalid input. Please enter a valid amount.')


class DepositHandler:
    def __init__(self, keybad, screen:Screen):        
        self.keybad = keybad
        self.screen = screen
        
    def handle(self, account):
        while True:
            try:
                amount = float(self.keybad.get_input('Enter the amout to deposit: '))
                if amount <= 0 :
                    self.screen.show_message('Invalid amount. Please Enter a positive number...')
                    continue
                transaction = DepositTransaction(amount)
                transaction.excute(account)
                break
            except ValueError:
                self.screen.show_message('Invalid input. Please enter a valid amount.')


class BalanceInquiryHandler:
    def handle(self, account):
        transaction = BalanceInquiryTransaction()
        transaction.excute(account)


class TranactionHistoryHandler:
    def handle(self, account:Account):
        account.display_transaction_history()


class TransferFundsHandler:
    def __init__(self, keybad, screen:Screen, bank):
        self.keybad = keybad
        self.screen = screen
        self.bank = bank
    
    def handle(self, account):
        while True:
            try:
                amount = float(self.keybad.get_input('Please enter the amount to transfer: '))
                if amount <= 0 :
                    self.screen.show_message('Invalid amount. Please enter a positive number...')
                    continue
                
                destination_account_number = self.keybad.get_input('Enter the destination account number: ')
                transaction = TransferTransaction(amount, destination_account_number)
                transaction.excute(account, self.bank)
                break
                
            except ValueError:
                self.screen.show_message('Invalid input. Please enter a valid amount.')  


class PinChangeHandler:
    def __init__(self, keybad, screen):
        self.keybad = keybad
        self.screen = screen
        
    def handle(self, account:Account):
        for _ in range(3):
            old_pin = self.keybad.get_input('Enter the old pin: ', secure=True)
            if account.linked_card and account.linked_card.get_pin() == old_pin:
                while True:
                    new_pin = self.keybad.get_input('Enter your new pin: ', secure=True)
                    confirm_new_pin = self.keybad.get_input('Confirm your new pin: ', secure=True)
                    if new_pin == confirm_new_pin:
                        self.screen.show_message('PIN changed successfully.')
                        return account.linked_card.set_pin(old_pin, new_pin)
                    self.screen.show_message('You entered anmatched confirm. Please try again.')
            else:
                self.screen.show_message('The old pin you entered is incorrect. Please Try again.')
        self.screen.show_message('You entered an incorrect pin three times. You can try again after 10 minutes. ')
        
        
from keybad import Keybad
from screen import Screen
from handlers import *

class AtmInterface:
    def __init__(self, bank, atm_location):
        self.bank = bank
        self.atm_location = atm_location
        self.keybad = Keybad()
        self.screen = Screen()
        self.withdraw_handler = WithdrawHandler(self.keybad, self.screen)
        self.deposit_handler = DepositHandler(self.keybad, self.screen)
        self.balance_inquiry_handler = BalanceInquiryHandler()
        self.transaction_history_handler = TranactionHistoryHandler()
        self.pin_change_handler = PinChangeHandler(self.keybad, self.screen)
        self.transfer_funds_handler = TransferFundsHandler(self.keybad, self.screen, self.bank)

    def display_main_menu(self, account):
        self.screen.show_message(f'Welcome to {self.bank.name} bank')
        main_menu = '''
    1. Withdraw
    2. Deposit
    3. Balance Inquiry
    4. View Transactions
    5. Change PIN
    6. Transfer Funds
    7. Exit
    Choose an option: '''
        while True: 
            user_choice = self.keybad.get_input(main_menu)
            match user_choice:
                case '1':
                    self.withdraw_handler.handle(account)
                case '2':
                    self.deposit_handler.handle(account)
                case '3':
                    self.balance_inquiry_handler.handle(account)
                case '4':
                    self.transaction_history_handler.handle(account)
                case '5':
                    self.pin_change_handler.handle(account)
                case '6':
                    self.transfer_funds_handler.handle(account)
                case '7':
                    self.screen.show_message('Ejecting Card...')
                    self.screen.show_message(f'Thank you for using {self.bank.name} bank.')
                    break
                case _:
                    self.screen.show_message('Invalid choice. Please try again.')
            self.keybad.get_input('Press any key to continue...')
            self.screen.clear_screen()
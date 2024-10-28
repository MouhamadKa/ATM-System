from abc import ABC, abstractmethod
import datetime
import os
from enum import Enum
import uuid


class Keybad:
    def get_input(self, message):
        return input(message)

        
class Bank:
    def __init__(self, name, bank_swift_code):
        self.name = name
        self.bank_code = bank_swift_code
        self.accounts = {}
        
    def add_customer(self, customer):
        # Here instead of adding the custimer himself, now I loop through all his accounts and add them to the bank
        for account in customer.accounts.values():
            self.accounts[account.account_number] = account
    
    
class Authenticator:
    def __init__(self, bank):
        self.bank = bank
        
    def authenticate(self, card_number, pin):
        for account in self.bank.accounts.values():
            if account.linked_card and account.linked_card.number == card_number and account.linked_card.get_pin() == pin:
                return account
        return None
    
    
class Customer:
    def __init__(self, name, address, phone_number, email):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.accounts = {}
        
    def add_account(self, account):
        self.accounts[account.account_number] = account
        
        
class Account:
    def __init__(self, number):
        self.account_number = number 
        self.balance = 0
        self.linked_card = None
        self.transaction_history = []
        
    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)
        
    def display_transaction_history(self):
        if self.transaction_history:
            for transaction in self.transaction_history:
                print(f'ID: {transaction.transaction_id} \nType: {transaction.transaction_type.value} {'\nAmount: '+ str(transaction.amount) if transaction.amount else ''} \nTimestamp:{transaction.timestamp}\n')
        else:
            print("You didn't made any transaction yet")
            
    def link_card(self, card):
        self.linked_card = card


class Card:
    def __init__(self, number, pin):
        self.number = number
        self.__pin = pin
    
    def get_pin(self):
        return self.__pin
    
    def set_pin(self, old_pin, new_pin):
        if old_pin == self.__pin:
            self.__pin = new_pin
            return True
        else:
            return False            
 
    
class CardReader:
    def __init__(self, atm, bank):
        self.bank = bank
        self.atm = atm
        
    def insert_card(self, card):
        pin = self.atm.keybad.get_input('Please enter your PIN: ')
        authenticator = Authenticator(self.bank)
        account =  authenticator.authenticate(card.number, pin)
        
        if account:
            self.atm.display_main_menu(account)
        else:
            self.atm.screen.show_message('Invalid card or PIN')
            return None
        
        
class Transaction(ABC):    
    def __init__(self, transaction_type, amount=None):
        self.transaction_id = uuid.uuid4()
        self.timestamp = datetime.datetime.now()
        self.transaction_type = transaction_type
        self.amount = amount
        
    @abstractmethod
    def excute(self):
        ...


class TransactionType(Enum):
        WITHDRAW = 'withdraw'
        DEPOSIT = 'deposit'
        BALANCE_INQUIRY = 'Balance Inquiry'
        TRANSFER = 'Transfer'
         

class WithdrawTransaction(Transaction):
    def __init__(self, amount):
        super().__init__(TransactionType.WITHDRAW, amount)
    
    def excute(self, account:Account):
        if account.balance >= self.amount:
            account.balance -= self.amount
            print(f'Withdrawl Successful.\nCurrent balance: {account.balance}')
            account.add_transaction(self)
        else:
            Transaction.transaction_counter -= 1
            print('Insufficient funds')
            
            
class DepositTransaction(Transaction):
    def __init__(self, amount):
        super().__init__(TransactionType.DEPOSIT, amount)
        
    def excute(self, account:Account):
        account.balance += self.amount
        print(f'Deposit Successful.\nCurrent balance: {account.balance}')
        account.add_transaction(self)
        

class BalanceInquiryTransaction(Transaction):
    def __init__(self):
        super().__init__(TransactionType.BALANCE_INQUIRY)
        
    def excute(self, account:Account):
        print(f'Your balance is {account.balance}')
        account.add_transaction(self)


class TransferTransaction(Transaction):
    ...


class Screen:
    def clear_screen(self):
        os.system('cls' if os.name=='nt' else 'clear')
        
    def show_message(self, message):
        print(message)


class ATM:
    def __init__(self, bank, atm_location):
        self.bank = bank
        self.atm_location = atm_location
        self.keybad = Keybad()
        self.screen = Screen()

    def display_main_menu(self, account):
        self.screen.show_message(f'Welcome to {self.bank.name} bank')
        main_menu = '''
    1. Deposit
    2. Withdraw
    3. Balance Inquiry
    4. View Transactions
    5. Exit
    Choose an option: '''
        while True: 
            user_choice = self.keybad.get_input(main_menu)
            if user_choice == '5':
                self.screen.show_message('Card Ejecting...')
                self.screen.show_message(f'Thank you for using {self.bank.name} bank.')
                break
            self.handle_transaction(user_choice, account)
    
    def handle_transaction(self, choice, account):
        try:
            match choice:
                case '1':
                    amount = float(self.keybad.get_input('Enter amount to deposit: '))
                    transaction = DepositTransaction(amount)
                    
                case '2':
                    amount = float(self.keybad.get_input('Enter amount to withdraw: '))
                    transaction = WithdrawTransaction(amount)
                    
                case '3':
                    transaction = BalanceInquiryTransaction()
                    
                case '4':
                    transaction = account.display_transaction_history()

                case _ :
                    transaction = self.screen.show_message('Invalid choice. Please enter a valid option from the list')
            
            if transaction:
                transaction.excute(account)
            self.keybad.get_input('\nPress any key to continue...')
            self.screen.clear_screen()
        except:
            self.screen.show_message('Invalid amount entered. Please try again')
        
my_bank = Bank('HSBC', 'HSBCEGXX')
customer1 = Customer('Mouhamad', 'bla bla', '0502143723', 'm@g.com')
account1 = Account('213124')
card1 = Card('9999999999999999', '0000')

customer1.add_account(account1)
my_bank.add_customer(customer1)

# print(account1.linked_card)
account1.link_card(card1)
# print(account1.linked_card)


atm = ATM(my_bank, 'hamada street')
card_reader = CardReader(atm, my_bank)
card_reader.insert_card(card1)

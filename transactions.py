from abc import ABC, abstractmethod
import datetime
import uuid
from enum import Enum
from account import Account

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
    def __init__(self, amount, destination_account_number):
        super().__init__(TransactionType.TRANSFER, amount)
        self.destination_account_number = destination_account_number        
        
    def excute(self, account, bank):
        self.account_number = account.account_number # I add this just to know it in the transaction history
        destination_account = bank.accounts.get(self.destination_account_number)
        if not destination_account:
            print("Destination Account Not Found")
            return False
        if self.amount > account.balance:
            print('Insufficient funds')
            return False
        account.balance -= self.amount
        account.add_transaction(self)
        destination_account.balance += self.amount
        destination_account.add_transaction(self)
        print(f'Transfer Successful.\nCurrent balance: {account.balance}')
        return True        
        

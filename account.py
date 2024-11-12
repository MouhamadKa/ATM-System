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
                if transaction.transaction_type.value != 'Transfer':
                    print(f'ID: {transaction.transaction_id} \nType: {transaction.transaction_type.value} \nAmount: {str(transaction.amount) if transaction.amount else ''} \nTimestamp:{transaction.timestamp}\n')
                else:
                    print(f'ID: {transaction.transaction_id} \nType: {transaction.transaction_type.value} \nFrom: {self.account_number} \nTo: {transaction.destination_account_number} \nAmount: {str(transaction.amount)} \nTimestamp:{transaction.timestamp}\n')
        else:
            print("You didn't made any transaction yet")
            
    def link_card(self, card):
        self.linked_card = card
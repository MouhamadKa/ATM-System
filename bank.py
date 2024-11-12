class Bank:
    def __init__(self, name, bank_swift_code):
        self.name = name
        self.bank_code = bank_swift_code
        self.accounts = {}
        
    def add_customer(self, customer):
        # Here instead of adding the custimer himself, now I loop through all his accounts and add them to the bank
        for account in customer.accounts.values():
            self.accounts[account.account_number] = account
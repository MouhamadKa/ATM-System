from bank import Bank
from customer import Customer
from account import Account
from card import Card
from atm import AtmInterface
from card_reader import CardReader
    
      
def main():
    my_bank = Bank('HSBC', 'HSBCEGXX')
    customer1 = Customer('Mouhamad', 'bla bla', '0502143723', 'm@g.com')
    account1 = Account('213124')
    account2 = Account('312412')
    card1 = Card('9999999999999999', '0000')

    customer1.add_account(account1)
    customer1.add_account(account2)
    my_bank.add_customer(customer1)

    # print(account1.linked_card)
    account1.link_card(card1)
    # print(account1.linked_card)


    atm = AtmInterface(my_bank, 'hamada street')
    card_reader = CardReader(atm)
    card_reader.insert_card(card1)
    #! Continue the transferfundshandler class and edit the whole project to edit and save changes in a csv file

if __name__ == '__main__':
    main()
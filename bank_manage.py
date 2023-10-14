class Bank:
    def __init__(self,name,address):
        self.name=name
        self.address=address
        self.users={}
        self.total_bal=0
        self.total_loan=0
        self.loan_feature=True
    def create_acc(self,name,email,addess,acc_typo):
        acc_nums=len(self.users)+1
        self.users[acc_nums]=User(name,email,addess,acc_typo)
        print(f"Account  created. Your account number is {acc_nums}.")
        return acc_nums
    def delete_acc(self,acc_nums):
        if acc_nums in self.users:
            del self.users[acc_nums]
    def toggle_loan_feature(self):
        self.loan_feature=not self.loan_feature
    def has_enough_bal(self,amount):
        return self.total_bal>=amount

class User:
    def __init__(self,name,email,addess,acc_typo):
        self.name=name
        self.email=email
        self.addess=addess
        self.acc_typo=acc_typo
        self.balance=0
        self.transaction_history=[]
        self.loan=0
    def deposit(self,amount):
        self.balance+=amount
        self.transaction_history.append(('deposit',amount))
    def withdraw(self,amount):
        if amount>self.balance:
            print('Withdrawal amount exceeded')
            return
        self.balance-=amount
        self.transaction_history.append(('withdraw',amount))
    def check_bal(self):
        return self.balance
    def check_transaction_history(self):
        return self.transaction_history
    def take_loan(self,bank,amount):
        if bank.loan_feature and self.loan_count<2 and bank.has_enough_bal(amount):
            bank.total_loan+=amount
            bank.total_bal-=amount
            self.balance+=amount
            self.loan_count+=1
            return True
        return False
    def transfer(self,bank,to_acc_nums,amount):
        if to_acc_nums not in bank.users or amount>self.balance:
            print("Transfer failed")
            return False
        bank.users[to_acc_nums].balance+=amount
        self.balance-=amount
        return True

class Admin(User):
    def __init__(self, name, email, addess, password):
        super().__init__(name, email, addess,'Admin')
        self.password=password
    def create_acc(self,bank,name,email,addess,acc_typo):
        if acc_typo not in ['Saving','Current']:
            print("Invalid account type.")
            return
        acc_nums=bank.create_acc(name,email,addess,acc_typo)
        print(f"Account created for {name}. The account number is {acc_nums}.")
        return acc_nums
    def delete_acc(self,bank,acc_nums):
        bank.delete_acc(acc_nums)
    def see_all_accs(self,bank):
        return bank.users
    def check_total_bal(self,bank):
        return bank.total_bal
    def check_total_loan(self,bank):
        return bank.total_loan
    def toggle_loan_feature(self,bank):
        bank.toggle_loan_feature()

def main():
    bank = Bank('My Bank','Capital')
    admin = Admin('Admin', 'admin@bank.com', 'Bank Address','123')

    while True:
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            password=input("Enter admin password: ")
            if password!=admin.password:
                print("Incorrect password!")
                continue
        
            print("1. Create Account")
            print("2. Delete Account")
            print("3. See All Accounts")
            print("4. Check Total Balance")
            print("5. Check Total Loan")
            print("6. Toggle Loan Feature")
            admin_choice = int(input("Enter your choice: "))

            if admin_choice == 1:
                name = input("Enter name: ")
                email = input("Enter email: ")
                address = input("Enter address: ")
                acc_typo = input("Enter account type (Saving/Current): ")
                admin.create_acc(bank, name, email, address, acc_typo)
            elif admin_choice == 2:
                account_number = int(input("Enter account number to delete: "))
                admin.delete_acc(bank, account_number)
            elif admin_choice == 3:
                accounts = admin.see_all_accs(bank)
                for account in accounts.values():
                    print(account.name, account.email, account.address, account.account_type)
            elif admin_choice == 4:
                print(admin.check_total_bal(bank))
            elif admin_choice == 5:
                print(admin.check_total_loan(bank))
            elif admin_choice == 6:
                admin.toggle_loan_feature(bank)

        elif choice == 2:
            acc_nums = int(input("Enter your account number: "))
            if acc_nums not in bank.users:
                print("Account does not exist.")
                continue
            user = bank.users[acc_nums]

            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Check Transaction History")
            print("5. Take Loan")
            print("6. Transfer Money")
            user_choice = int(input("Enter your choice: "))

            if user_choice == 1:
                amount = float(input("Enter amount to deposit: "))
                user.deposit(amount)
            elif user_choice == 2:
                amount = float(input("Enter amount to withdraw: "))
                user.withdraw(amount)
            elif user_choice == 3:
                print(user.check_bal())
            elif user_choice == 4:
                for transaction in user.check_transaction_history():
                    print(transaction)
            elif user_choice == 5:
                amount = float(input("Enter loan amount: "))
                if not user.take_loan(bank, amount):
                    print("Loan feature is off or you have already taken two loans.")
            elif user_choice == 6:
                to_acc_nums = int(input("Enter the account number to transfer money to: "))
                amount = float(input("Enter amount to transfer: "))
                if not user.transfer(bank, to_acc_nums, amount):
                    print("Transfer failed.")

        elif choice == 3:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
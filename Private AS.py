#This is an example of a class with a private variable in Python. The private variable is denoted by the double underscore prefix (__).
#In this case, the account password is a private variable, and it can only be accessed through a public method (get_password) defined
#in the class. Attempting to access the private variable directly from outside the class will raise an AttributeError.

class Account:
    def __init__(self, account_id, account_name, __acc_password):
        self.account_id = account_id
        self.account_name = account_name
        self.__acc_password = __acc_password

    def display_account_info(self):
        print(f"Account ID: {self.account_id}, Account Name: {self.account_name}")

    def __set_password(self, new_password):
        self.__acc_password = new_password

    def get_password(self):
        return self.__acc_password


c1 = Account(101, "John Doe", input("Enter account password: "))
c1.display_account_info()
print(f"Account Password: {c1.get_password()}") #this will work because we are accessing the private variable through a public method.
c1.__set_password(input("Enter new account password: "))  # This will raise an AttributeError because __set_password is private.

print(c1.__acc_password)  # This will raise an AttributeError because __acc_password is private.

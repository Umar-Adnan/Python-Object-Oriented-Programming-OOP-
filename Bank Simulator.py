from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_holder: str, initial_balance: float):
        self._account_holder = account_holder  # Protected attribute
        self.__balance = max(0.0, initial_balance)  # Private attribute

    @abstractmethod
    def deposit(self, amount: float) -> bool:
        """Process a deposit to the account."""
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Process a withdrawal from the account."""
        pass

    #Controlled getter for private balance
    def get_balance(self) -> float:
        return self.__balance

    # Internal helper methods for sub-classes to safely alter private balance
    def _add_to_balance(self, amount: float):
        self.__balance += amount

    def _subtract_from_balance(self, amount: float):
        self.__balance -= amount

    def display_statement(self):
        print(f"Account Holder: {self._account_holder} | Current Balance: ${self.__balance:.2f}")


class SavingsAccount(BankAccount):
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        super().__init__(account_holder, initial_balance)

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        self._add_to_balance(amount)
        print(f"Successfully deposited ${amount:.2f}.")
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.get_balance():
            print("Insufficient funds!")
            return False
        self._subtract_from_balance(amount)
        print(f"Successfully withdrew ${amount:.2f}.")
        return True


# -------------------------------------------------------------------
# INTERACTIVE APPLICATION / SIMULATOR
# -------------------------------------------------------------------
def run_bank_simulator():
    print("=" * 40)
    print("      WELCOME TO PYTHON BANK APP      ")
    print("=" * 40)

    name = input("Enter your name to open an account: ").strip()
    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount ($): "))
            if initial_deposit < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric value.")

    account = SavingsAccount(account_holder=name, initial_balance=initial_deposit)
    print(f"\nAccount created for {name}!")

    while True:
        print("\n--- MENU ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            account.display_statement()

        elif choice == "2":
            try:
                amt = float(input("Enter deposit amount: $"))
                account.deposit(amt)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "3":
            try:
                amt = float(input("Enter withdrawal amount: $"))
                account.withdraw(amt)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            print("\nThank you for banking with us. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    run_bank_simulator()
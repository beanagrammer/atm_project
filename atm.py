import asyncio

class Account:
    def __init__(self, account_id, balance, pin):
        self.account_id = account_id
        self.balance = balance
        self.pin = pin

    async def check_password(self, input_pin):
        """
         The primary purpose of adding asynchronous functionality here is to showcase how it might handle asynchronous operations,
         which can be very useful when integrating with actual back-end systems or databases.
        """
        # Simulating some asynchronous operation, like checking the PIN with a back-end system
        await asyncio.sleep(1)  # Sleep for 1 second for simulation purposes
        return self.pin == input_pin

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class ATMController:
    def __init__(self, bank):
        self.bank = bank
        self.current_account = None
        self.card_inserted = False
        self.is_authenticated = False

    def insert_card(self, account_id):
        account = self.bank.get_account(account_id)
        if not account:
            raise ValueError("Invalid card")
        self.card_inserted = True
        self.current_account = account

    def eject_card(self):
        print("Card ejected.")
        self.card_inserted = False
        self.is_authenticated = False
        self.current_account = None

    async def enter_pin(self, pin):
        if not self.current_account or not self.card_inserted:
            raise ValueError("No card inserted or account selected")
        if await self.current_account.check_password(pin):
            self.is_authenticated = True
            return True
        return False


    def _ensure_authenticated(self):
        if not self.is_authenticated:
            raise PermissionError("Not authenticated")

    def display_balance(self):
        self._ensure_authenticated()
        return self.current_account.get_balance()

    def deposit(self, amount):
        self._ensure_authenticated()
        self.current_account.deposit(amount)

    def withdraw(self, amount):
        self._ensure_authenticated()
        self.current_account.withdraw(amount)


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.atm_controller = ATMController(self)

    def add_account(self, account_id, balance, pin):
        self.accounts[account_id] = Account(account_id, balance, pin)

    def get_account(self, account_id):
        return self.accounts.get(account_id)




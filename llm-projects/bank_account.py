from datetime import datetime, timedelta
import json


class BankAccount:
    """Base bank account class"""

    # Class attribute - shared across all instances
    bank_name = "State Bank of Kundan"
    _next_account_number = 1001

    def __init__(self, owner: str, initial_deposit: float = 0):
        if not self.is_valid_amount(initial_deposit):
            raise ValueError("Initial deposit must be non-negative")

        self.owner = owner
        self._balance = initial_deposit
        self.account_number = BankAccount._next_account_number
        BankAccount._next_account_number += 1
        self.history = []
        self._log("OPEN", initial_deposit)

    @property
    def balance(self) -> float:
        """Read-only balance - use deposit/withdraw to change."""
        return self._balance

    @staticmethod
    def is_valid_amount(amount: float) -> bool:
        return isinstance(amount, (int, float)) and amount >= 0

    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        acct_type = data.get("type", "BankAccount")
        owner = data["owner"]
        balance = data.get("balance", 0)
        if acct_type == "SavingsAccount":
            return SavingsAccount(owner, balance, interest_rate=data.get("interest_rate", 0.04))
        if acct_type == "CheckingAccount":
            return CheckingAccount(owner, balance, overdraft_limit=data.get("overdraft_limit", 5000))
        return BankAccount(owner=owner, initial_deposit=balance)

    def deposit(self, amount: float):
        if amount <= 0 or not isinstance(amount, (int, float)):
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._log("DEPOSIT", amount)

    def withdraw(self, amount: float):
        if amount <= 0 or not isinstance(amount, (int, float)):
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._log("WITHDRAW", amount)

    def _log(self, action: str, amount: float):
        self.history.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "action": action,
                "amount": amount,
                "balance": self._balance,
            }
        )

    def __str__(self):
        return f"BankAccount(owner={self.owner}, balance={self.balance:.2f})"

    def monthly_statement(self, days: int = 30):
        """Print history entries from the last `days` days (default 30)."""
        cutoff = datetime.now() - timedelta(days=days)
        print(f"--- Monthly statement (last {days} days) for {self.owner} ---")
        for entry in self.history:
            ts_str = entry.get("timestamp")
            if not ts_str:
                continue
            try:
                ts = datetime.fromisoformat(ts_str)
            except Exception:
                continue
            if ts >= cutoff:
                print(entry)

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance:.2f})"

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False
        return self.account_number == other.account_number

    def transfer(self, other: "BankAccount", amount: float):
        if not isinstance(other, BankAccount):
            raise TypeError("Transfer target must be a BankAccount")
        if amount <= 0 or not isinstance(amount, (int, float)):
            raise ValueError("Transfer amount must be positive")
        # Use withdraw/deposit so subclasses' rules (e.g. overdraft) apply
        self.withdraw(amount)
        other.deposit(amount)

    def to_dict(self) -> dict:
        """Serialize account to a dict for JSON storage."""
        data = {"type": self.__class__.__name__, "owner": self.owner, "balance": self._balance}
        # include subclass-specific fields
        if isinstance(self, SavingsAccount):
            data["interest_rate"] = getattr(self, "interest_rate", 0.04)
        if isinstance(self, CheckingAccount):
            data["overdraft_limit"] = getattr(self, "overdraft_limit", 5000)
        return data

    def __lt__(self, other: object) -> bool:
        """Allow sorting accounts by balance: sorted(accounts)."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance


class SavingsAccount(BankAccount):
    """Earns interest. Cannot go below zero."""

    def __init__(
        self, owner: str, initial_deposit: float = 0, interest_rate: float = 0.04
    ):
        super().__init__(owner, initial_deposit)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        self._log("INTEREST", interest)


class CheckingAccount(BankAccount):
    """Allows overdraft up to a limit."""

    def __init__(
        self, owner: str, initial_deposit: float = 0, overdraft_limit: float = 5000
    ):
        super().__init__(owner, initial_deposit)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        if amount <= 0 or not isinstance(amount, (int, float)):
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance + self.overdraft_limit:
            raise ValueError("Exceeds overdraft limit")
        self._balance -= amount
        self._log("WITHDRAW", amount)


class Bank:
    """Container for multiple `BankAccount` instances."""

    def __init__(self, name: str = "Unnamed Bank"):
        self.name = name
        self.accounts: list[BankAccount] = []

    def add_account(self, account: BankAccount):
        if not isinstance(account, BankAccount):
            raise TypeError("account must be a BankAccount")
        self.accounts.append(account)

    def remove_account(self, account: BankAccount):
        self.accounts.remove(account)

    @property
    def total_assets(self) -> float:
        """Sum of balances of all accounts held by the bank."""
        return sum(acc.balance for acc in self.accounts)

    def __repr__(self):
        return f"Bank(name={self.name!r}, total_assets={self.total_assets:.2f})"

    def save_to_file(self, path: str):
        """Save all accounts to a JSON file at `path`."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump([acc.to_dict() for acc in self.accounts], f, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "Bank":
        """Load accounts from a JSON file and return a Bank instance."""
        bank = cls()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            acct = BankAccount.from_dict(item)
            bank.add_account(acct)
        return bank


if __name__ == "__main__":
    # Create accounts
    kundan = SavingsAccount("Kundan", 10000, interest_rate=0.05)
    friend = CheckingAccount("Aman", 2000, overdraft_limit=3000)

    print(kundan)
    print(friend)

    # Transactions
    kundan.deposit(5000)
    kundan.withdraw(2000)
    kundan.transfer(friend, 3000)
    kundan.add_interest()

    # Overdraft
    friend.withdraw(4000)

    print("\n--- After transactions ---")
    print(kundan)
    print(friend)

    # History
    print("\n--- Kundan's history ---")
    for entry in kundan.history:
        print(entry)

    # Demo: monthly statement (last 30 days)
    print()
    kundan.monthly_statement()

    # Demo: bank holding multiple accounts
    bank = Bank("State Bank of Kundan")
    bank.add_account(kundan)
    bank.add_account(friend)
    print()
    print(bank)
    print("Total assets:", bank.total_assets)

    # Save bank accounts to JSON
    bank.save_to_file("accounts.json")
    print("Saved accounts.json")

    # Load into a new bank and show totals
    loaded = Bank.load_from_file("accounts.json")
    print("Loaded:", loaded)

    # Test from_dict
    new_acc = BankAccount.from_dict({"owner": "Ravi", "balance": 7500})
    print("\n", new_acc)

    # Test equality
    print("\nSame account?", kundan == friend)

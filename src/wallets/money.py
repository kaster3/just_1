from src.wallets.exceptions import NegativeValueException, NotComparisonException


class Money:
    def __init__(self, value: float, currency: str) -> None:
        self.value = value
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise NotComparisonException("Невозможно сложить значения разных валют")
        return Money(currency=self.currency, value=self.value + other.value)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise NotComparisonException("Невозможно вычесть значения разных валют")
        if self.value - other.value < 0:
            raise NegativeValueException("Resulting value cannot be negative")
        return Money(currency=self.currency, value=self.value - other.value)

    def __eq__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            raise NotComparisonException("Невозможно сравнить типы")
        return self.value == other.value and self.currency == other.currency


class Wallet:
    def __init__(self, money: Money) -> None:
        self._currencies = {money.currency: money}

    @property
    def currencies(self):
        return list(self._currencies.keys())

    def get(self, currency: str) -> Money:
        return self._currencies.get(currency, Money(value=0, currency=currency))

    def __getitem__(self, currency: str) -> Money:
        return self.get(currency)

    def __delitem__(self, currency: str) -> None:
        if currency in self._currencies:
            del self._currencies[currency]

    def __len__(self) -> int:
        return len(self._currencies)

    def __contains__(self, currency: str) -> bool:
        return currency in self._currencies

    def add(self, money: Money) -> "Wallet":
        if money.currency in self._currencies:
            self._currencies[money.currency] += money
        else:
            self._currencies[money.currency] = money
        return self

    def sub(self, money: Money) -> "Wallet":
        if money.currency in self._currencies:
            self._currencies[money.currency] -= money
        else:
            raise ValueError(f"Currency {money.currency} not in wallet")
        return self

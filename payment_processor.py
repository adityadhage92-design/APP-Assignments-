"""
=====================================================================
 CONFIGURABLE PAYMENT PROCESSING SYSTEM
 Design Pattern Used: STRATEGY PATTERN
=====================================================================
Purpose : Let the caller select / switch / configure the payment
          method (Credit Card, PayPal, UPI, Net Banking) at RUN TIME
          without changing the PaymentProcessor's code.

---------------------------------------------------------------------
IN PLAIN ENGLISH \u2014 what's actually going on here:

  Think of a shop counter. The cashier (PaymentProcessor) doesn't
  care HOW you pay, only THAT you can pay. Each payment method
  (CreditCardPayment, PayPalPayment, UPIPayment, NetBankingPayment)
  follows the same simple rule book (PaymentStrategy): it must be
  able to validate() its own details and pay() the amount.

  Want to add a new payment method later, like a wallet or crypto
  option? Write ONE new class that follows the rule book. Nothing
  else in this file needs to change.

  Want to switch which method is active right now? Call
  processor.set_strategy(new_method) \u2014 or build one ready-made
  by name via PaymentProcessor.create("upi", upi_id=...).
=====================================================================
"""


import functools
import uuid
from abc import ABC, abstractmethod
from datetime import datetime


# =====================================================================
# 1. CROSS-CUTTING DECORATOR (transaction logging)
# =====================================================================

def log_transaction(func):
    """Decorator: logs the start and result of every payment attempt."""
    @functools.wraps(func)
    def wrapper(self, amount, *args, **kwargs):
        method = self.strategy.name if self.strategy else "NONE"
        print(f"[LOG] Initiating payment of Rs.{amount:.2f} via {method}")
        result = func(self, amount, *args, **kwargs)
        print(f"[LOG] Transaction {result.txn_id} -> {result.status}")
        return result
    return wrapper


# =====================================================================
# 2. RECEIPT  (simple value object returned after every payment)
# =====================================================================

class Receipt:
    """Represents the outcome of a payment attempt."""

    def __init__(self, txn_id, amount, method, status):
        self.txn_id = txn_id
        self.amount = amount
        self.method = method
        self.status = status
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"----- PAYMENT RECEIPT -----\n"
                f"Txn ID   : {self.txn_id}\n"
                f"Method   : {self.method}\n"
                f"Amount   : Rs.{self.amount:.2f}\n"
                f"Status   : {self.status}\n"
                f"Time     : {self.timestamp:%Y-%m-%d %H:%M:%S}\n"
                f"----------------------------")

    def __repr__(self):
        return f"Receipt(txn_id={self.txn_id!r}, status={self.status!r})"


# =====================================================================
# 3. STRATEGY INTERFACE
#    Every concrete payment method MUST implement validate() and pay()
#    Plain English: this is the "rule book" every payment method
#    agrees to follow, so the Context never has to know which one
#    it's actually talking to.
# =====================================================================

class PaymentStrategy(ABC):
    """The common Strategy interface all payment methods implement."""

    name = "Generic Payment"

    @abstractmethod
    def validate(self):
        """Return True if the supplied payment details look valid."""

    @abstractmethod
    def pay(self, amount):
        """Process the payment and return a Receipt."""

    def _make_receipt(self, amount, status="SUCCESS"):
        return Receipt(txn_id=str(uuid.uuid4())[:8], amount=amount,
                        method=self.name, status=status)


# =====================================================================
# 4. CONCRETE STRATEGIES
# =====================================================================

class CreditCardPayment(PaymentStrategy):
    name = "Credit Card"

    def __init__(self, card_number, cvv, expiry):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def validate(self):
        return self.card_number.isdigit() and len(self.card_number) == 16 and len(self.cvv) == 3

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(amount, status="FAILED - Invalid Card Details")
        print(f"  -> Charging Rs.{amount:.2f} to card ending {self.card_number[-4:]}")
        return self._make_receipt(amount)


class PayPalPayment(PaymentStrategy):
    name = "PayPal"

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        return "@" in self.email and len(self.password) >= 6

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(amount, status="FAILED - Invalid PayPal Credentials")
        print(f"  -> Redirecting to PayPal account {self.email} to pay Rs.{amount:.2f}")
        return self._make_receipt(amount)


class UPIPayment(PaymentStrategy):
    name = "UPI"

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def validate(self):
        return "@" in self.upi_id

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(amount, status="FAILED - Invalid UPI ID")
        print(f"  -> Requesting Rs.{amount:.2f} from UPI ID {self.upi_id}")
        return self._make_receipt(amount)


class NetBankingPayment(PaymentStrategy):
    name = "Net Banking"

    def __init__(self, bank_name, account_number):
        self.bank_name = bank_name
        self.account_number = account_number

    def validate(self):
        return self.account_number.isdigit() and len(self.account_number) >= 9

    def pay(self, amount):
        if not self.validate():
            return self._make_receipt(amount, status="FAILED - Invalid Account Number")
        print(f"  -> Debiting Rs.{amount:.2f} from {self.bank_name} A/C {self.account_number}")
        return self._make_receipt(amount)


# =====================================================================
# 5. CONTEXT CLASS  (the "configurable" part of the system)
#    Plain English: this is the "cashier". It holds whichever payment
#    method is active right now and simply asks it to do the work.
# =====================================================================

class PaymentProcessor:
    """The Strategy-pattern Context. Holds a reference to the CURRENT
    PaymentStrategy and delegates the real work to it. The strategy
    can be swapped ('configured') at any time via set_strategy(),
    or looked up dynamically from a registry via create()."""

    _registry = {}   # e.g. "upi" -> UPIPayment   (name -> strategy class)

    def __init__(self, strategy: PaymentStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        """Swap the payment strategy at run time."""
        self.strategy = strategy
        print(f"[CONFIG] Payment method switched to: {strategy.name}")

    @log_transaction
    def process_payment(self, amount):
        if self.strategy is None:
            raise ValueError("No payment strategy configured on this processor")
        return self.strategy.pay(amount)

    # ---------------- classmethods: registry-driven configuration -----
    @classmethod
    def register_strategy(cls, key, strategy_cls):
        """Register a new payment method under a short key, e.g. 'upi'."""
        cls._registry[key] = strategy_cls
        print(f"[REGISTRY] '{key}' -> {strategy_cls.__name__} registered")

    @classmethod
    def available_methods(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, key, **kwargs):
        """Factory helper: build a PaymentProcessor already configured
        with the strategy registered under `key`, e.g.
        PaymentProcessor.create('upi', upi_id='user@bank')."""
        if key not in cls._registry:
            raise ValueError(f"No payment strategy registered under '{key}'")
        strategy_cls = cls._registry[key]
        return cls(strategy_cls(**kwargs))


# =====================================================================
# 6. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    # ---- Step A: register available strategies (classmethod) ---------
    PaymentProcessor.register_strategy("credit_card", CreditCardPayment)
    PaymentProcessor.register_strategy("paypal", PayPalPayment)
    PaymentProcessor.register_strategy("upi", UPIPayment)
    PaymentProcessor.register_strategy("netbanking", NetBankingPayment)

    print("\nAvailable payment methods:", PaymentProcessor.available_methods())

    # ---- Step B: create a processor pre-configured via the registry --
    processor = PaymentProcessor.create("upi", upi_id="rahul@okhdfcbank")
    receipt1 = processor.process_payment(1500)
    print(receipt1)

    # ---- Step C: swap strategy at run time (set_strategy) -------------
    print("\n--- switching to Credit Card ---")
    processor.set_strategy(CreditCardPayment("1234567812345678", "123", "12/27"))
    receipt2 = processor.process_payment(2500)
    print(receipt2)

    # ---- Step D: try an invalid configuration --------------------------
    print("\n--- switching to (invalid) PayPal ---")
    processor.set_strategy(PayPalPayment("bad-email", "123"))
    receipt3 = processor.process_payment(500)
    print(receipt3)

    # ---- Step E: switch to Net Banking ---------------------------------
    print("\n--- switching to Net Banking ---")
    processor.set_strategy(NetBankingPayment("State Bank", "987654321"))
    receipt4 = processor.process_payment(999.50)
    print(receipt4)

"""Digital wallet demonstration for static code analysis."""
import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.getenv("GATEWAY_SECRET", "")
WALLET_PIN = "4321"
wallet = {"balance": 0.0}
wallet = {"balance": 0.0, "daily_limit": 1000}
transactions = []


def hash_pin(pin, salt):
    """Hash a PIN using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode(),
        salt,
        200_000
    )


def add_money(amount, source="UPI", log=None):
    """Add money to the wallet and record the credit transaction."""
    if amount <= 0:
        return False

    if log is None:
        log = []

    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat(),
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Update the wallet's daily payment limit."""
    wallet["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Process a merchant payment after verifying the PIN."""
    salt = b"digital_wallet_demo_salt"
    stored_hash = hash_pin(WALLET_PIN, salt)
    entered_hash = hash_pin(pin, salt)

    if not hmac.compare_digest(entered_hash, stored_hash):
        print("Wrong PIN for payment to", merchant)
        return False

    if (
        amount <= 0
        or amount > wallet["balance"]
        or amount > wallet["daily_limit"]
    ):
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat()
    })
    return True


def mini_statement(count=3):
    """Print the most recent wallet transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type):
    """Calculate cashback for a transaction."""
    if merchant_type == "health":
        return round(amount * 0.02, 2)
    return 0.0


def check_gateway(secret):
    """Check whether the supplied gateway secret matches."""
    return secret == GATEWAY_SECRET


def receipt_path():
    """Create and return a safe temporary receipt-file path."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    ) as receipt_file:
        return receipt_file.name


def main():
    """Run the digital wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()

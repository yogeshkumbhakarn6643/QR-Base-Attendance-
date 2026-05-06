from services.billing_service import add_payment, get_wallet_balance

add_payment(1, 500)
print("Balance:", get_wallet_balance(1))
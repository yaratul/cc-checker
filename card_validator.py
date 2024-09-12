import re

def luhn_check(card_number):
    """Check if a card number is valid using the Luhn algorithm."""
    digits = [int(d) for d in str(card_number)]
    checksum = 0
    odd_even = len(digits) % 2

    for count, digit in enumerate(digits):
        if count % 2 == odd_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return (checksum % 10) == 0

def validate_card_format(card_data):
    """Validate card format: cc_number|mm|yyyy|cvc."""
    pattern = r'^\d{13,19}\|\d{2}\|\d{4}\|\d{3,4}$'
    if re.match(pattern, card_data):
        parts = card_data.split('|')
        card_number, month, year, cvc = parts
        if luhn_check(card_number):
            print(f"Card {card_number} is valid.")
            return True
        else:
            print(f"Card {card_number} failed Luhn check.")
    else:
        print(f"Card format is incorrect: {card_data}")
    return False

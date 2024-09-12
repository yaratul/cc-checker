# main.py

import re
import yaml
import logging
from stripe_handler import initialize_stripe, process_verification_charge  # Correct import statement

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        filename='stripe_tool.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config():
    """Load configuration from a YAML file."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

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
            logging.info(f"Card {card_number[-4:]} passed Luhn check.")
            return True
        else:
            logging.error(f"Card {card_number[-4:]} failed Luhn check.")
    else:
        logging.error(f"Card format is incorrect: {card_data}")
    return False

def main():
    """Main application logic."""
    setup_logging()
    config = load_config()

    sk_key = input("Enter your Stripe secret key: ")

    if not initialize_stripe(sk_key):
        print("Invalid API key. Exiting.")
        return

    with open('cards.txt', 'r') as file:
        for line in file:
            card_data = line.strip()
            if validate_card_format(card_data):
                process_verification_charge(card_data)

if __name__ == "__main__":
    main()


# --------------------------------------------- DE --------------------------------------------- #
# Fragt nach Input für Account 1/2, wenn ungültig dann erneute Abfrage

# --------------------------------------------- ENG --------------------------------------------- #
# Asks for input for account 1/2, if invalid then renewed query

def get_account_choice():
    choice = input("Eingabe: ").strip()
    if choice not in ["1", "2"]:
        print("Ungültige Eingabe! Bitte 1 oder 2.")
        return get_account_choice()
    return choice

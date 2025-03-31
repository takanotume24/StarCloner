def get_user_confirmation() -> bool:
    """
    Get user confirmation from input.
    """
    choice = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"

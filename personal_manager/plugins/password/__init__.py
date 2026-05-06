from personal_manager.core.plugin import Plugin

class PasswordPlugin(Plugin):
    @property
    def name(self) -> str:
        return "Password Manager"

    @property
    def description(self) -> str:
        return "Securely store and manage your passwords."

    def run(self) -> None:
        print("\n--- Password Manager ---")
        print("This feature is under development.")
        input("Press Enter to return...")

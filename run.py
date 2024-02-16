import getpass
import json
import locale
from datetime import datetime, date

class DateEncoder(json.JSONEncoder):
  def default(self, obj):
      """
      This class is an extension of json.JSONEncoder.
      This customizes the default method to enable specific serialization for date objects.
      During the JSON encoding process, date objects are transformed into their ISO format representation.
      """
      if isinstance(obj, date):
          return obj.isoformat()  # Serialize date objects to ISO format
      return super().default(obj)

class PennyProvisions:
  CURRENCY_OPTIONS = {
    '1': ('USD', 'US Dollar'),
    '2': ('EUR', 'Euro'),
    '3': ('GBP', 'British Pound Sterling'),
    '4': ('JPY', 'Japanese Yen'),
    '5': ('AUD', 'Australian Dollar'),
    '6': ('CAD', 'Canadian Dollar'),
    '7': ('CHF', 'Swiss Franc'),
    '8': ('CNY', 'Chinese Yuan'),
    '9': ('SEK', 'Swedish Krona'),
    '10': ('NZD', 'New Zealand Dollar'),
    '11': ('INR', 'Indian Rupee'),
    '12': ('BRL', 'Brazilian Real'),
    '13': ('ZAR', 'South African Rand'),
    '14': ('COP', 'Colombian Peso'),
    '15': ('PEN', 'Peruvian Sol'),
    '16': ('ILS', 'Israeli New Shekel'),
  }

  def __init__(self):
      """
      Initialize Penny Provisions budgeting tool
      """
      self.user_data_file = "user_data.json"
      self.load_user_data()
      self.selected_currency = None  # Saves the users selected currency

  def load_user_data(self):
      """
      Load user data from the JSON file.
      """
      try:
          with open(self.user_data_file, 'r') as file:
              file_content = file.read()
              if not file_content.strip():
                  # File is empty
                  self.user_data = {}
                  return

              data = json.loads(file_content)
              # Convert target_date strings back to datetime.date objects
              for _username, user_info in data.items():
                  if "target_date" in user_info and isinstance(user_info["target_date"], str):
                      user_info["target_date"] = datetime.strptime(user_info["target_date"], "%Y-%m-%d").date()

              self.user_data = data
      except FileNotFoundError:
          self.user_data = {}

  def save_user_data(self):
      """
      Save user data to the JSON file
      """
      data_to_save = self.user_data.copy()

      with open(self.user_data_file, 'w') as file:
          json.dump(data_to_save, file, indent=4, cls=DateEncoder)

  def authenticate_user(self):
    """
    Authenticates the user's inputted username and password.
    """
    if not self.user_data:
        print("No user credentials found. Please set up an account first.")
        return None

    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        if username in self.user_data and self.user_data[username]["password"] == password:
            return username
        else:
            print("Invalid credentials. Please try again or enter 'cancel' to go back to the main menu.")
            choice = input("Enter 'cancel' to return to the main menu: ")
            if choice.lower() == 'cancel':
                return None
    
  def account_creation(self):
    """
    Set up a new user account by creating a username and password.
    Once the account is created, the user will need to log in using the details provided.
    """
    username = input("Create a username: ")
    password = getpass.getpass("Create a password: ")

    if username in self.user_data:
        print("Username already exists. Please choose a different one.")
        return

    # Prompt for currency selection
    print("\nSelect your preferred currency:")
    for key, value in self.CURRENCY_OPTIONS.items():
        print(f"{key}. {value}")

    selected_currency = None
    while not selected_currency:
        currency_choice = input("Enter the number corresponding to your preferred currency: ")

        if currency_choice in self.CURRENCY_OPTIONS:
            selected_currency = self.CURRENCY_OPTIONS[currency_choice]
            self.selected_currency = selected_currency  # Store the selected currency
        else:
            print("Invalid choice. Please enter a valid number from the options.")

    # Initialize incomes and expenditures lists in JSON
    self.user_data[username] = {
        "password": password,
        "savings_target": 0,
        "current_savings": 0,
        "expenses": [],
        "incomes": [],
        "expenditures": [],
        "currency": selected_currency,
        "debts": [],
        "savings_goals": {}
    }

    self.save_user_data()
    print("Account successfully created!")

  def view_current_savings(self, username):
    """
    Display the current savings for each savings goal.
    """
    user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))

    savings_goals = self.user_data[username].get("savings_goals", {})

    if not savings_goals:
        print("No savings goals found. Please create a savings goal.")
        return

    user_currency_symbol = user_currency[1]  # Get the currency symbol
    print(f"\nCurrent Savings ({user_currency_symbol}):")
    for goal_name, goal_info in savings_goals.items():
        current_savings = goal_info["current_savings"]
        print(f"{goal_name}: {user_currency[0]}{current_savings:.2f}")

  def get_valid_amount(self, prompt):
    """
    Ensures that the amount inputted by the user is a positive amount.
    In the event a negative amount is inputted, the user is prompted to input a valid amount.
    """
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                raise ValueError("Amount cannot be negative.")
            return amount
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive number.")

  INCOME_OPTIONS = {
      '1': 'Employment',
      '2': 'Self-employment',
      '3': 'Benefits',
      '4': 'Grants/support payments',
      '5': 'Pension',
      '6': 'Rental income',
      '7': 'Employment benefits',
      '8': 'Interest on savings',
      '9': 'Trust distributions',
      '10': 'Insurance payouts',
      '11': 'Capital gains',
      '12': 'Child maintenance',
      '13': 'Bonus/Commission',
      '14': 'Royalties',
      '15': 'Gifts',
      '16': 'Dividends',
      '17': 'Other',
  }

  EXPENDITURE_OPTIONS = {
      '1': 'Rent payments',
      '2': 'Mortgage payments',
      '3': 'Insurance premiums',
      '4': 'Loan repayments',
      '5': 'Debt',
      '6': 'Food',
      '7': 'Utilities',
      '8': 'Transport',
      '9': 'Entertainment',
      '10': 'Travel/vacation',
      '11': 'Non-essentials',
      '12': 'Toiletries',
      '13': 'Dining out',
      '14': 'Bills',
      '15': 'Housing cost',
      '16': 'Clothing',
      '17': 'Capital',
      '18': 'Operational costs',
      '19': 'Tax',
      '20': 'Other'
  }  

  def main(self):
    """
    Main function to run Penny Provisions program.
    """
    print("Welcome to Penny Provision!")

    while True:
        print("\nMain Menu:")
        print("1. Log In")
        print("2. Set Up Account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice.lower() == 'cancel':
            print("Operation canceled.")
            break

        if choice == "1":
            username = self.authenticate_user()
            if username:
                selected_goal = None  # Store the selected savings goal

                print(f"Logged in as {username}.")
                while True:
                    print("\nPenny Provisions Menu:")
                    print("1. Add Savings Goal")
                    print("2. Select Savings Goal")
                    print("3. Record Income")
                    print("4. Record Expenditure")
                    print("5. View Recommendations")
                    print("6. View Current Savings")
                    print("7. Manage Debts")  # Added option
                    print("8. View All Savings Goals")
                    print("9. Analyze Monthly Activity")
                    print("10. Log Out")

                    option = input("Enter your choice (1-10): ")

                    if option.lower() == 'cancel':
                        print("Operation canceled.")
                        break

                    if option == "1":
                        self.add_savings_goal(username)
                    elif option == "2":
                        selected_goal = self.select_savings_goal(username)
                        if selected_goal:
                            print(f"Savings goal '{selected_goal}' selected.")
                    elif option == "3":
                        if selected_goal:
                            self.record_income(username, selected_goal)
                        else:
                            print("Please select a savings goal first.")
                    elif option == "4":
                        if selected_goal:
                            self.record_expenditure(username)
                        else:
                            print("Please select a savings goal first.")
                    elif option == "5":
                        if selected_goal:
                            self.calculate_recommendation(username, selected_goal)
                        else:
                            print("Please select a savings goal first.")
                    elif option == "6":
                        self.view_current_savings(username)
                    elif option == "7":
                        self.manage_debts(username)  # Added method call
                    elif option == "8":
                        self.view_all_savings_goals(username)
                    elif option == "9":
                        self.analyze_monthly_activity(username)
                    elif option == "10":
                        confirm_logout = input("Are you sure you want to log out? (yes/no): ")
                        if confirm_logout.lower() == 'yes':
                            break
                        elif confirm_logout.lower() == 'no':
                            continue
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print("Invalid choice. Please enter a number between 1 and 10.")

        elif choice == "2":
            self.account_creation()

        elif choice == "3":
            print("Exiting Penny Provisions. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    penny_provisions = PennyProvisions()
    penny_provisions.main()  
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
      # Write mode to create a user if they do not currently exist
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
        username = input("Enter your username:\n")
        password = getpass.getpass("Enter your password: ")

        if username in self.user_data and self.user_data[username]["password"] == password:
            return username
        else:
            print("Invalid credentials. Hit enter to try again or enter 'cancel' to go back to the main menu.")
            choice = input("Enter 'cancel' to return to the main menu:\n")
            if choice.lower() == 'cancel':
                return None
    
  def account_creation(self):
    """
    Set up a new user account by creating a username and password.
    Once the account is created, the user will need to log in using the details provided.
    """
    username = input("Create a username:\n")
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
        currency_choice = input("Enter the number corresponding to your preferred currency:\n")

        if currency_choice in self.CURRENCY_OPTIONS:
            selected_currency = self.CURRENCY_OPTIONS[currency_choice]
            self.selected_currency = selected_currency  # Store the selected currency
        else:
            print("Invalid choice. Please enter a valid number from the options.")

    # Initialize incomes and expenses lists in JSON
    self.user_data[username] = {
        "password": password,
        "savings_target": 0,
        "current_savings": 0,
        "expenses": [],
        "incomes": [],
        "expenses": [],
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

    user_currency_symbol = user_currency[1]  # Get the currency type
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

  EXPENSE_OPTIONS = {
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

  def add_savings_goal(self, username):
    """
    Adds a new savings goal for the user.
    """
    print("Enter 'cancel' to cancel.")
    goal_name = input("Enter the name of your savings goal:\n")

    if goal_name.lower() == 'cancel':
        print("Savings goal creation canceled.")
        return

    target_amount = float(input("Enter your savings target amount:\n"))
    target_date_str = input("Enter the date you wish to save the required money by (YYYY-MM-DD):\n")
    
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    # Check if the target date is in the past
    if target_date < datetime.now().date():
        print("Target date cannot be in the past.")
        return

    # Check if the key is present in the user_data, if not, create it
    if "savings_goals" not in self.user_data[username]:
        self.user_data[username]["savings_goals"] = {}

    self.user_data[username]["savings_goals"][goal_name] = {
        "target_amount": target_amount,
        "target_date": target_date,
        "current_savings": 0,
        "expenses": []
    }
    self.save_user_data()
    print(f"Savings goal '{goal_name}' added successfully!")

  def select_savings_goal(self, username):
    """
    Allows the user to select a savings goal.
    """
    user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))
    savings_goals = self.user_data[username].get("savings_goals", {})

    if not savings_goals:
        print("No savings goals found.")
        return None

    print("Select a savings goal:")
    for i, (goal_name, goal_info) in enumerate(savings_goals.items(), start=1):
        print(f"{i}. {goal_name} - Target Amount: {user_currency[0]}{goal_info['target_amount']:.2f}")

    choice = input("Enter the number corresponding to the savings goal (or type 'cancel' to go back):\n")

    if choice.lower() == 'cancel':
        return None

    try:
        choice_index = int(choice)
        if 1 <= choice_index <= len(savings_goals):
            selected_goal = list(savings_goals.keys())[choice_index - 1]
            return selected_goal
        else:
            print("Invalid choice. Please enter a number within the given range.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

  def record_income(self, username, selected_goal):
    """
    Records inputted income data for the user, ensuring a valid amount is entered.
    Records income input date for incorporation into Google Sheets API.
    Updates current savings based on inputs.
    """
    user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))

    while True:
        print("Income Options:")
        for key, value in self.INCOME_OPTIONS.items():
            print(f"{key}. {value}")

        choice = input("Enter the number corresponding to the income source (or type 'done' to finish):\n")

        if choice.lower() == 'done':
            break

        if choice in self.INCOME_OPTIONS:
            income_type = self.INCOME_OPTIONS[choice]
            try:
                income_amount = self.get_valid_amount(f"Enter the amount for {income_type}: ")
                income_date_str = input("Enter the date of income (YYYY-MM-DD):\n")
                income_date = datetime.strptime(income_date_str, "%Y-%m-%d").date()

                # Date validation check
                if income_date > datetime.now().date():
                    print("Error: Cannot record income for a future date.")
                    continue

                # Update savings for the selected goal
                self.user_data[username]["current_savings"] += income_amount
                self.user_data[username]["savings_goals"][selected_goal]["current_savings"] += income_amount

                # Capture income details including date and associated savings goal
                income_details = {"type": income_type, "amount": income_amount, "date": income_date,
                                  "goal": selected_goal}
                self.user_data[username]["incomes"].append(income_details)

                self.save_user_data()
                print(f"Income recorded successfully! Current savings: {user_currency[0]}{self.user_data[username]['current_savings']:.2f}")
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid positive number.")
        else:
            print("Invalid choice. Please enter a number from the options.")

  def record_expense(self, username):
    """
    Records inputted expense data for the user, ensuring a valid amount is entered.
    Records expense input date for tracking purposes.
    Updates expense details based on inputs.
    """
    while True:
        print("\nEnter 'done' when finished.")
        print("\nSelect the type of expense:")
        for key, value in self.EXPENSE_OPTIONS.items():
            print(f"{key}. {value}")

        expense_choice = input("Enter the number corresponding to the type of expense:\n")

        if expense_choice == 'done':
            break

        if expense_choice in self.EXPENSE_OPTIONS:
            expense_type = self.EXPENSE_OPTIONS[expense_choice]

            try:
                expense_amount = self.get_valid_amount(f"Enter the amount for {expense_type}: ")

                expense_date_str = input("Enter the date of the expense (YYYY-MM-DD):\n")
                expense_date = datetime.strptime(expense_date_str, "%Y-%m-%d").date()

                # Date validation check
                if expense_date > datetime.now().date():
                    print("Error: Cannot record expense for a future date.")
                    continue

                # Capture expense details including date
                expense_details = {"type": expense_type, "amount": expense_amount,
                                       "date": expense_date}
                self.user_data[username].setdefault("expenses", []).append(expense_details)

                self.save_user_data()
                print(
                    f"expense recorded successfully! Total expense: £{self.calculate_total_expenses(username):.2f}")

                # Ask the user if they want to add another expense
                add_another = input("Do you want to add another expense? (yes/no):\n")
                if add_another.lower() != 'yes':
                    break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid positive number.")
        else:
            print("Invalid choice. Please enter a valid number from the options.")

  def add_debt_expense_to_savingsgoal(self, username):
    """
    Records inputted debt data for the user, ensuring a valid amount is entered.
    Records expense to savings goal.
    This could be a debt that is not added to the manage debts.
    Updates debt details based on inputs.
    """
    while True:
        print("Enter 'done' when finished.")
        debt_type = input("Enter the type of debt:\n")
        if debt_type.lower() == 'done':
            break

        try:
            debt_amount = self.get_valid_amount(f"Enter the amount for {debt_type}: ")
            debt_name = input(f"Enter a name for the {debt_type}:\n")
            debt_date_str = input("Enter the date of the debt (YYYY-MM-DD):\n")
            debt_date = datetime.strptime(debt_date_str, "%Y-%m-%d").date()

            # Date validation check
            if debt_date > datetime.now().date():
                print("Error: Cannot record debt for a future date.")
                continue

            # Capture debt details including date
            debt_details = {"type": debt_type, "amount": debt_amount, "name": debt_name, "date": debt_date}
            self.user_data[username].setdefault("debts", []).append(debt_details)

            self.save_user_data()
            print(f"Debt recorded successfully! Total debt: £{self.calculate_total_debt(username):.2f}")

            # Ask the user if they want to add another debt
            add_another = input("Do you want to add another debt? (yes/no):\n")
            if add_another.lower() != 'yes':
                break
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive number.")

  def calculate_total_expense(self, username):
    """
    Calculates and returns the total expense for the user.
    """
    total_expense = sum(expense["amount"] for expense in self.user_data[username].get("expenses", []))
    return total_expense

  def calculate_recommendation(self, username, selected_goal):
    """
    Calculates and displays savings recommendations based on the users selected savings goal.
    This function collates information about the selected savings goal including:
    Target amount, Current savings, Expenses, Incomes and target date.
    The recommended weekly, monthly and annual savings amount is displayed.
    If the savings target is reached then a message will be displayed to confirm this.
    """
    user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))
    goal_info = self.user_data[username]["savings_goals"][selected_goal]
    target_amount = goal_info["target_amount"]
    current_savings = goal_info["current_savings"]
    target_date = goal_info.get("target_date", None)

    remaining_days = None  # Initialize remaining_days here

    if current_savings >= target_amount:
        print(f"\nCongratulations! Your savings goal '{selected_goal}' has already been achieved.")
    elif target_date:
        if isinstance(target_date, date):
            remaining_days = (target_date - datetime.now().date()).days
        elif isinstance(target_date, str):
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            remaining_days = (target_date - datetime.now().date()).days

    if target_amount > 0 and remaining_days:
        weekly_recommendation = (target_amount - current_savings) / (remaining_days / 7)
        monthly_recommendation = (target_amount - current_savings) / (remaining_days / 30)
        annually_recommendation = (target_amount - current_savings) / (remaining_days / 365)

        user_currency_symbol = user_currency[1]  # Get the currency symbol
        print(f"\nRecommendations ({user_currency_symbol}):")
        print(f" - Weekly: Save {user_currency[0]}{max(weekly_recommendation, 0):.2f} per week.")
        print(f" - Monthly: Save {user_currency[0]}{max(monthly_recommendation, 0):.2f} per month.")
        print(f" - Annually: Save {user_currency[0]}{max(annually_recommendation, 0):.2f} per year.")

  def view_all_savings_goals(self, username):
      """
      Display all savings goals along with their details.
      """
      user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))
      savings_goals = self.user_data[username].get("savings_goals", {})

      if not savings_goals:
          print("No savings goals found.")
          return

      user_currency_symbol = user_currency[1]  # Get the currency symbol
      print(f"\nAll Savings Goals ({user_currency_symbol}):")
      for goal_name, goal_info in savings_goals.items():
          print(f"\nGoal: {goal_name}")
          print(f"  Target Amount: {user_currency[0]}{goal_info['target_amount']:.2f}")
          print(f"  Target Date: {goal_info.get('target_date', 'N/A')}")
          print(f"  Current Savings: {user_currency[0]}{goal_info['current_savings']:.2f}")

          # Display expenses associated with the goal
          expenses = goal_info.get('expenses', [])
          if expenses:
              print("  Expenses:")
              for expense in expenses:
                  print(f"    - {expense['type']}: {user_currency[0]}{expense['amount']:.2f} on {expense['date']}")

      print("\nEnd of Savings Goals List.")

  def analyze_monthly_activity(self, username):
    """
    Analyze monthly activity to find the month with the most expenses and savings.
    """
    incomes = self.user_data[username].get("incomes", [])
    expenses = self.user_data[username].get("expenses", [])

    # Combine incomes and expenses
    all_activities = incomes + expenses

    # Create a dictionary to store monthly totals
    monthly_totals = {}

    for activity in all_activities:
        # Extract the month and year from the date
        if isinstance(activity["date"], date):
            month_year = activity["date"].strftime("%Y-%m")
        elif isinstance(activity["date"], str):
            month_year = datetime.strptime(activity["date"], "%Y-%m-%d").strftime("%Y-%m")
        else:
            continue  # Skip this activity if date format is not recognized

        # Initialize or update the monthly total
        if month_year not in monthly_totals:
            monthly_totals[month_year] = {"income": 0, "expense": 0}

        if activity in incomes:
            monthly_totals[month_year]["income"] += activity["amount"]
        else:
            monthly_totals[month_year]["expense"] += activity["amount"]

    if not monthly_totals:
        print("No monthly activity found.")
        return

    # Find the month with the highest income and expense
    max_income_month = max(monthly_totals, key=lambda x: monthly_totals[x]["income"], default=None)
    max_expense_month = max(monthly_totals, key=lambda x: monthly_totals[x]["expense"], default=None)

    print("\nMonthly Activity Analysis:")
    if max_income_month:
        print(f"Month with the highest income: {max_income_month} - £{monthly_totals[max_income_month]['income']:.2f}")
    else:
        print("No income recorded.")

    if max_expense_month:
        print(f"Month with the highest expense: {max_expense_month} - £{monthly_totals[max_expense_month]['expense']:.2f}")
    else:
        print("No expense recorded.")

  def manage_debts(self, username):
    """
    Manage Debts Menu.
    Allows the user to manage debts (add or view).
    """
    user_currency = self.user_data[username].get("currency", ('GBP', 'British Pound Sterling'))

    while True:
        user_currency_symbol = user_currency[1]  # Get the currency symbol
        print(f"\nManage Debts Menu ({user_currency_symbol}):")
        print("1. Add Debt")
        print("2. View Debts")
        print("3. Add Payment To Debt")
        print("4. Go Back")

        option = input("Enter your choice (1-4):\n")

        if option == "1":
            self.add_debt(username)
        elif option == "2":
            self.view_all_debts(username)
        elif option == "3":
            self.add_repayment_to_debt(username)
        elif option == "4":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

  def add_debt(self, username):
    """
    Allows the user to add a new debt.
    """
    print("Enter 'done' when finished.")
    while True:
        try:
            debt_amount = self.get_valid_amount("Enter the amount for the debt: ")
            debt_name = input("Enter a name for the debt:\n")
            debt_type = input("Enter the type of debt:\n")

            # Term is when the debt needs to be paid off by
            debt_term = int(input("Enter the term of the debt (in months):\n"))
            interest_rate = float(input("Enter the interest rate on the debt (as a percentage):\n"))

            # Capture debt details including term and interest
            debt_details = {
                "amount": debt_amount,
                "term": debt_term,
                "name": debt_name,
                "type": debt_type,
                "interest_rate": interest_rate,
                "payments": []  # List to store payment details
            }
            self.user_data[username].setdefault("debts", []).append(debt_details)

            self.save_user_data()
            print(f"Debt recorded successfully! Total debt: £{self.calculate_total_debt(username):.2f}")

            # Ask the user if they want to add another debt
            add_another = input("Do you want to add another debt? (yes/no):\n")
            if add_another.lower() != 'yes':
                  break
        except ValueError as e:
            print(f"Error: {e}. Please enter valid information.")

  def view_all_debts(self, username):
    """
    Display all debts along with their details.
    """
    debts = self.user_data.get(username, {}).get("debts", [])

    if not debts:
        print("No debts found.")
        return

    print("\nAll Debts:")
    for debt in debts:
        print(f"\nName: {debt.get('name', 'N/A')}")

        # Calculate and print amount paid
        amount_paid = sum(payment["amount"] for payment in debt.get("payments", []))
        print(f"Amount Paid: £{amount_paid:.2f}")

        # Calculate and print remaining balance
        remaining_balance = self.calculate_remaining_balance(debt)
        print(f"Remaining Balance: £{remaining_balance:.2f}")

        # Display individual payments and their details
        if debt.get("payments"):
            print("Payments:")
            for payment in debt["payments"]:
                print(f"  - Amount: £{payment['amount']:.2f} - Date: {payment['date']}")

        print("------")

    print("\nEnd of Debts List.")

  def add_repayment_to_debt(self, username):
    """
    Records an repayment towards a specific debt.
    """
    while True:
        print("\nSelect a debt to add an expense:")
        debts = self.user_data[username].get("debts", [])
        if not debts:
          print("No debts found. Please add a debt first.")
          return

        for i, debt in enumerate(debts, start=1):
            print(f"{i}. {debt['name']} - Type: {debt['type']} - Remaining Term: {debt['term']} months")

        choice = input("Enter the number corresponding to the debt (or type 'cancel' to go back):\n")

        if choice.lower() == 'cancel':
            return

        try:
            choice_index = int(choice)
            if 1 <= choice_index <= len(debts):
                selected_debt = debts[choice_index - 1]
                debt_name = selected_debt['name']
                expense_amount = self.get_valid_amount(f"Enter the amount for the expense on {debt_name}: ")

                # Record the expense details including the date
                expense_date_str = input("Enter the date of the expense (YYYY-MM-DD):\n")
                expense_date = datetime.strptime(expense_date_str, "%Y-%m-%d").date()

                # Add a date validation check
                if expense_date > datetime.now().date():
                    print("Error: Cannot record expense for a future date.")
                    continue

                # Update the debt details with the expense
                selected_debt["payments"].append({"amount": expense_amount, "date": expense_date})

                self.save_user_data()
                print(f"expense recorded successfully! Remaining debt on {debt_name}: £{self.calculate_remaining_balance(selected_debt):.2f}")
            else:
                print("Invalid choice. Please enter a number within the given range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

  def calculate_total_debt(self, username):
    """
    Calculate the total debt for user.
    """
    total_debt = 0
    debts = self.user_data.get(username, {}).get("debts", [])

    for debt in debts:
      total_debt += debt.get("amount", 0)

      return total_debt

  def calculate_remaining_balance(self, debt):
    """
    Calculates the remaining balance on a debt.
    """
    amount_paid = sum(payment["amount"] for payment in debt.get("payments", []))
    remaining_balance = debt["amount"] + (debt["amount"] * debt["interest_rate"] / 100) - amount_paid
    return max(remaining_balance, 0)

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

        choice = input("Enter your choice (1-3):\n")

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
                    print("4. Record Expense")
                    print("5. View Recommendations")
                    print("6. View Current Savings")
                    print("7. Manage Debts")
                    print("8. View All Savings Goals")
                    print("9. Analyze Monthly Activity")
                    print("10. Log Out")

                    option = input("Enter your choice (1-10):\n")

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
                            self.record_expense(username)
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
                        self.manage_debts(username)
                    elif option == "8":
                        self.view_all_savings_goals(username)
                    elif option == "9":
                        self.analyze_monthly_activity(username)
                    elif option == "10":
                        confirm_logout = input("Are you sure you want to log out? (yes/no):\n")
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
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

  
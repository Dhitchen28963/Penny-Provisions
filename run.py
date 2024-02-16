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
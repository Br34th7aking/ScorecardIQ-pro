import sqlite3

def insert(query): 
  try:
    
      # Connect to DB and create a cursor
      sqliteConnection = sqlite3.connect('/Users/abhijitraj/Documents/ScorecardIQ-pro/db.sqlite3')

      cursor = sqliteConnection.cursor()
      try:
         cursor.execute(query)
         sqliteConnection.commit()
      except Exception as e: 
         print("Exception", e) 
      

  
      # Close the cursor
      cursor.close()

  # Handle errors
  except sqlite3.Error as error:
      print('Error occurred - ', error)
  
  # Close DB Connection irrespective of success
  # or failure
  finally:
    
      if sqliteConnection:
          sqliteConnection.close()


def execute(query): 
  try:
    
      # Connect to DB and create a cursor
      sqliteConnection = sqlite3.connect('/Users/abhijitraj/Documents/ScorecardIQ-pro/db.sqlite3')

      cursor = sqliteConnection.cursor()
      try:
         cursor.execute(query)
      except Exception as e: 
         print("Exception", e) 
      
      result = cursor.fetchall()
  
      # Close the cursor
      cursor.close()
      return result

  # Handle errors
  except sqlite3.Error as error:
      print('Error occurred - ', error)
  
  # Close DB Connection irrespective of success
  # or failure
  finally:
    
      if sqliteConnection:
          sqliteConnection.close()
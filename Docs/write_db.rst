Database Operations
===================

This module contains functions to perform database operations such as creating a SQLite database and writing data into it.

Database Operation Steps
-------------------------

Write data from a pandas DataFrame to a SQLite database.

Args
  db_name (str): The path to the SQLite database file.

  df (DataFrame): A pandas DataFrame containing data to be written into the database.

.. code-block:: python

    def write_db(db_name, df):
        try:
            conn = sq.connect(db_name) 
            df.to_sql(db_name, conn, if_exists='replace', index=False)  # writes to file
            conn.close()
            logger.info("Database write operation completed.")
        except Exception as error:
            logger.error(f"Error during database write operation: {error}")

Main Program
------------

Main program to write data from a CSV file to a SQLite database.

.. code-block:: python

   if __name__ == "__main__":
    db_name = path.abspath(path.join(path.dirname(__file__), './assignment.sqlite'))
    df = pd.read_csv(path.abspath(path.join(path.dirname(__file__), '../data/hp_oltis_sanctioned_budget.csv')))
    write_db(db_name, df)

      

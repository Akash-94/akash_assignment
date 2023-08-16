import pandas as pd
import sqlite3 as sq
from os import path
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='database_operations.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def write_db(db_name, df):
    '''creates a db and writes the data into that database'''

    logger = logging.getLogger("DatabaseOperations")
    logger.info("Starting database write operation...")

    try:
        conn = sq.connect(db_name) 
        df.to_sql(db_name, conn, if_exists='replace', index=False)  # writes to file
        conn.close()
        logger.info("Database write operation completed.")
    except Exception as error:
        logger.error(f"Error during database write operation: {error}")


if __name__ == "__main__":
    db_name = path.abspath(path.join(path.dirname(__file__), './assignment.sqlite'))
    df = pd.read_csv(path.abspath(path.join(path.dirname(__file__), '../data/hp_oltis_sanctioned_budget.csv')))
    write_db(db_name, df)


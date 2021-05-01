import sqlite3
import time
import pandas as pd
import streamlit as st
from .utils import norm_df_dtypes, setup_logger

logger = setup_logger()


class Database:
    def __init__(self, file_name: str = "database.sqlite"):

        # Create SQLITE3 Database
        self.conn = sqlite3.connect(file_name)
        logger.info({"message": "Database object created.",
                    "file_name": file_name})

    def add_table(self, df: pd.DataFrame, table_name: str, norm_dtypes: bool = True):
        """
        Add new table to SQLite3 database.

        Arguments:
        - df: DataFrame that will be converted to a table.
        - table_name: The table name in the database.
        """
        logger.info({"message": "Add new table", "df size": len(df),
                     "table_name": table_name, "norm_dtypes": norm_df_dtypes})

        try:
            if norm_dtypes:
                df = norm_df_dtypes(df)
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            st.success("Table created.")
            time.sleep(0.3)
            st.experimental_rerun()
        except Exception as error:
            logger.error(error)
            st.sidebar.error(error)

        logger.info({"message": "New table added."})

    def drop_table(self, table_name: str):
        """
        Delete a table in SQLite3 database.

        Arguments:
        - table_name: The name of table that you want to delete.
        """
        logger.info({"message": "Droping table", "table_name": table_name})

        try:
            cursor = self.conn.cursor()
            cursor.execute("DROP TABLE {}".format(table_name))
            st.success("Table deleted.")
            time.sleep(0.3)
            st.experimental_rerun()
        except Exception as error:
            logger.error(error)
            st.sidebar.error(error)

        logger.info({"message": "Table dropped."})

    def show_tables(self):
        """
        Return tables in the database.
        """
        logger.info({"message": "Show tables query."})
        return self.query("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")

    def query(self, query: str):
        """
        Run query at database.

        Arguments:
        - query: SQL query
        """
        logger.info({"message": "Running SQL query in database."})
        try:
            df = pd.read_sql(query, self.conn, parse_dates=[
                             'DATA_INICIAL', 'DATA_FINAL', 'DATA_VEICULACAO'])
            df = norm_df_dtypes(df)

            logger.info({"message": "Query finished.", "df size": len(df)})

            return df
            
        except Exception as error:
            logger.error(error)
            st.error(error)
            st.stop()

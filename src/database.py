import sqlite3
import time
import pandas as pd
import streamlit as st

class Database:
    def __init__(self, file_name: str = "sqlite.db"):

        # Create SQLITE3 Database
        self.conn = sqlite3.connect(file_name)

    def add_table(self, df = pd.DataFrame, table_name: str = "table"):
        """
        Add new table to SQLite3 database.

        Arguments:
        - df: DataFrame that will be converted to a table.
        - table_name: The table name in the database.
        """
        try:
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            st.success("Table created.")
            time.sleep(0.3)
            st.experimental_rerun()
        except Exception as error:
            st.sidebar.error(error)
            
    def drop_table(self, table_name: str = "table"):
        """
        Delete a table in SQLite3 database.

        Arguments:
        - table_name: The name of table that you want to delete.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DROP TABLE {}".format(table_name))
            st.success("Table deleted.")
            time.sleep(0.3)
            st.experimental_rerun()

        except Exception as error:
            st.sidebar.error(error)

    def query(self, query: str):
        """
        Run query at database.

        Arguments:
        - query: SQL query
        """
        try:
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as error:
            st.error(error)
            st.stop()
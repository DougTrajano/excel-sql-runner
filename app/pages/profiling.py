import logging
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from src.database import Database

logger = logging.getLogger(__name__)

def profiling_page(state):
    logger.info({"message": "Loading profiling_page"})
    st.title("Profiling Tables")

    # Select table
    db = Database(file_name=state.db_name)
    db_tables = db.query("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")

    if len(db_tables) == 0:
        st.warning("The database has no tables available.")
        logger.warning({"message": "The database has no tables available."})
        st.stop()

    st.write("You can select a table in the list below or create your custom SQL-statement.")
    
    table = st.selectbox('Table', options=db_tables,
                         help="Select a table in the database.")

    with st.beta_expander("SQL-statement"):
        query = st.text_area("SQL-statement", value="SELECT * FROM {}".format(table),
                             height=300,
                             help="SQL-statement based on SQLite syntax.")
    st.write(' ')

    if st.button("Profiling"):
        logger.info({"message": "Profiling Table."})
        db = Database(file_name=state.db_name)
        df_query = db.query(query)

        pr = ProfileReport(df_query, explorative=True)
        st_profile_report(pr)

    state.sync()

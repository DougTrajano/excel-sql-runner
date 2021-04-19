import logging
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from src.database import Database

logger = logging.getLogger(__name__)

def profiling_page(state):
    logger.info({"message": "Loading profiling page."})
    st.title("Profiling Tables")

    # Select table
    db = Database(file_name=state.db_name)
    db_tables = db.show_tables()

    if len(db_tables) == 0:
        st.warning("The database has no tables available.")
        logger.warning({"message": "The database has no tables available."})
        st.stop()

    st.write("You can select a table in the list below or create your custom SQL-statement.")
    
    query = st.text_area("SQL-statement", value="SELECT * FROM table",
                            height=300,
                            help="SQL-statement based on SQLite syntax.")
                             
    st.write(' ')
    
    if st.button("Profiling"):
        logger.info({"message": "Profiling Table."})

        df_query = db.query(query)

        pr = ProfileReport(df_query, explorative=True, dark_mode=True)
        st_profile_report(pr)

    logger.info({"message": "Profiling page loaded."})
    state.sync()

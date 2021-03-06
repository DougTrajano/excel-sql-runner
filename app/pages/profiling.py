import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from src.database import Database
from src.utils import setup_logger

logger = setup_logger()


def profiling_page():
    logger.info({"message": "Loading profiling page."})
    st.title("Profiling Tables")

    # Select table
    db = Database(file_name=st.session_state.db_name)
    db_tables = db.show_tables()

    if len(db_tables) == 0:
        st.warning("The database has no tables available.")
        logger.warning({"message": "The database has no tables available."})
        st.stop()

    st.write("You can select an entire table or create your custom SQL-statement.")
    
    with st.form(key="profiling_form"):
        query = st.text_area("SQL-statement", value="SELECT * FROM table",
                                height=300,
                                help="SQL-statement based on SQLite syntax.")
                                
        st.write(' ')
    
        if st.form_submit_button(label='Profiling'):
            logger.info({"message": "Profiling Table."})

            df_query = db.query(query)
        else:
            df_query = None

    if df_query is not None:
        pr = ProfileReport(df_query, explorative=True, dark_mode=True)
        st_profile_report(pr)

    logger.info({"message": "Profiling page loaded."})
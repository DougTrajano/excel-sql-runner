import streamlit as st
import logging
from src.database import Database
from src.utils import excel_download_link

logger = logging.getLogger(__name__)

def home_page(state):
    logger.info({"message": "Loading home page."})
    st.title("Excel SQL Runner")

    st.write("Here you can run SQLs on your excel files.")
    st.write("You can use `Add table` in sidebar menu to upload your excel files to temporary database.")

    # Create Database object
    db = Database(file_name=state.db_name)

    query = st.text_area("SQL-statement", value="SELECT * FROM table",
                         height=300,
                         help="SQL-statement based on SQLite syntax.")

    if st.button("Run query"):
        logger.info({"message": "Running query"})

        df_query = db.query(query)
        
        st.markdown(excel_download_link(df_query), unsafe_allow_html=True)
        st.write(df_query.head(1000))
        st.write("Displaying first 1000 rows.")
    
    logger.info({"message": "Home page loaded."})
    state.sync()
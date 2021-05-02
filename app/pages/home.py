import streamlit as st
from src.database import Database
from src.utils import setup_logger, excel_download_link

logger = setup_logger()


def home_page(state):
    logger.info({"message": "Loading home page."})
    st.title("Excel SQL Runner")

    st.write("Here you can run SQLs on your excel files.")
    st.write("You can use `Add table` in sidebar menu to upload your excel files to temporary database.")

    # Create Database object
    db = Database(file_name=state.db_name)

    with st.form(key="home_form"):
        query = st.text_area("SQL-statement", value="SELECT * FROM table",
                            height=300,
                            help="SQL-statement based on SQLite syntax.")

        if st.form_submit_button(label='Run query'):
            logger.info({"message": "Running query"})

            df_query = db.query(query)
        else:
            df_query = None

    if df_query is not None:
        st.markdown(excel_download_link(df_query), unsafe_allow_html=True)

        if len(df_query) > 1000:
            st.write(df_query.head(1000))
            st.write("Displaying first 1000 rows.")
        else:
            st.write(df_query)
            st.write("Displaying {} rows.".format(len(df_query)))
    
    logger.info({"message": "Home page loaded."})
    state.sync()
import streamlit as st
import logging
from src.database import Database
from src.utils import download_link

logger = logging.getLogger(__name__)

def home_page(state):
    st.title("Excel SQL Runner")
    db = Database(file_name=state.db_name)

    query = st.text_area("SQL-statement", value="SELECT * FROM table",
                         height=300,
                         help="SQL-statement based on SQLite syntax.")

    if st.button("Run query"):
        logger.info({"message": "Running query"})
        df_query = db.query(query)

        file_link = download_link(object_to_download=df_query,
                                  download_filename="{}.csv".format(
                                      state.db_name),
                                  download_link_text="Download file")
        st.markdown(file_link, unsafe_allow_html=True)

        st.write(df_query.head(1000))
        st.write("Displaying first 1000 rows.")

    state.sync()
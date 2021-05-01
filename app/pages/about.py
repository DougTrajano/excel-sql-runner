import streamlit as st
from src.utils import setup_logger

logger = setup_logger()

def about_page(state):
    logger.info({"message": "Loading about page."})
    st.title("About Excel SQL Runner")
    
    st.write("A data app that allows you to run SQL in excel files. :)")
    st.write("You can create tables in a temporary database to aggregate, joins and all transformation available in SQL.")

    
    st.subheader("Data Privacy")
    st.markdown("""
    No data will be transferred outside the application when executed locally.

    If you use the instantiated application, the data will be transferred and temporarily stored on the server.
    """)

    st.subheader("Terms of use")
    st.write("This application and the source code is a hobby project and have no warranties in this use.")

    state.sync()
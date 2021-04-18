import logging
import streamlit as st

logger = logging.getLogger(__name__)

def about_page(state):
    logger.info({"message": "Loading about page."})
    st.title("About this project")
    
    st.write("PROJECT_DESC")

    st.subheader("Motivation")
    st.write("MOTVATION_DESC")
    
    st.subheader("Data Privacy")
    st.write("PRIVACY_DESC")

    st.subheader("Terms of use")
    st.write("This application and the source code is a hobby project and have no warranties in this use.")

    state.sync()
import logging
import datetime
import pandas as pd
import streamlit as st
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
from src.database import Database

logger = logging.getLogger(__name__)

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """

    def __init__(self):

        logger.info({"message": "Instantiate MultiApp object."})

        self.apps = []

    def add_page(self, title, func):
        """Adds a new page to application.
        Parameters
        ----------
        title:
            title of the app. Appears in the dropdown in the sidebar.
        func:
            the python function to render this app.
        """

        logger.info({"message": "Adding page to app.", "title": title})

        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, page_title: str = None, page_icon: str = None, disable_menu: bool = False):

        logger.info({"message": "Starting MultiApp."})

        state = _get_state()

        st.set_page_config(page_title=page_title, layout="wide",
                            page_icon=page_icon)

        st.sidebar.title(page_title)
        
        if disable_menu:
            self.disable_menu()

        app = st.sidebar.radio(
            ' ',
            self.apps,
            format_func=lambda app: app['title'])

        if st.sidebar.button("Clear session"):
            state.clear()

        # Define unique name
        if state.db_name is None:
            logger.info({"message": "Defining database name"})
            state.db_name = str(int(datetime.datetime.now().timestamp())) + ".sqlite"
        db = Database(file_name=state.db_name)

        with st.sidebar.beta_expander('Add table'):
            add_table = st.text_input("Table name", value="table",
                                    help="The name of table that you want to create based on this file.",
                                    key="add_table")

            uploaded_file = st.file_uploader("Upload file",
                                            type=["xlsx"],
                                            help="Import excel file.")

            if st.button("Add table"):
                df = pd.read_excel(uploaded_file)
                db.add_table(df, add_table)

        with st.sidebar.beta_expander("Drop table"):
            del_table = st.text_input("Table name", value="table",
                                    help="The name of table that you want to delete.",
                                    key="del_table")

            if st.button("Drop table"):
                db.drop_table(del_table)

        with st.sidebar.beta_expander("Show tables"):
            result = db.query("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
            st.table(result)

        app['function'](state)

        state.sync()

    def disable_menu(self):
        logger.info({"message": "Disabling Streamlit's menu."})
        hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)


class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(
            self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state
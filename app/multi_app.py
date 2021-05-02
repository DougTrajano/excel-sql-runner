import datetime
import pandas as pd
import streamlit as st
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
from src.database import Database
from src.utils import setup_logger

logger = setup_logger()


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

    def add_page(self, page_title: str, func):
        """Adds a new page to application.

        Arguments:
        - page_title: Page title used by sidebar menu.
        - func: the python function to render this app.            
        """

        logger.info({"message": "Adding page to app.", "title": page_title})

        self.apps.append({
            "title": page_title,
            "function": func
        })

    def run(self, app_title: str = None, page_icon: str = None, disable_menu: bool = False):
        """
        Run Streamlit Data App.

        Arguments:
        - page_title: Data App title
        - page_icon: Data App favicon.
        - disable_menu: Disable Streamlit menu (recommend to production environment).
        """
        logger.info({"message": "Starting MultiApp."})

        state = _get_state()

        st.set_page_config(page_title=app_title, layout="wide",
                           page_icon=page_icon)

        st.sidebar.title(app_title)

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
            uploaded_file = st.file_uploader("Upload file",
                                             type=["xlsx"],
                                             help="Import excel file.")

            if uploaded_file is not None:
                # Check sheet_names
                xl = pd.ExcelFile(uploaded_file)

                if len(xl.sheet_names) > 1:
                    sheet_name = st.selectbox('Sheet name',
                                              options=xl.sheet_names,
                                              help='Sheet name is the excel tab.')
                else:
                    sheet_name = xl.sheet_names[0]

                add_table = st.text_input("Table name",
                                          value=sheet_name,
                                          help="Table that will be creatd in database.",
                                          key="add_table")

            if st.button("Add table"):
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                db.add_table(df, add_table)

        tables = db.show_tables()
        tables = tables['name'].tolist()

        if len(tables) > 0:
            with st.sidebar.beta_expander("Drop table"):
                del_table = st.selectbox('Table name', tables,
                                            help="The name of table that you want to delete.",
                                            key="del_table")

                if st.button("Drop table"):
                    db.drop_table(del_table)

            with st.sidebar.beta_expander("Show tables"):
                for table in tables:
                    st.write('- {}'.format(table))

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

        elif self._state["hash"] is not None and self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
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

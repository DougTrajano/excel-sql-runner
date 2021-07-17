import datetime
import pandas as pd
import streamlit as st
from src.database import Database
from src.utils import setup_logger, remove_files_by_extension

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

        # App configs
        st.set_page_config(page_title=app_title,
                           layout="wide",
                           page_icon=page_icon)

        st.sidebar.title(app_title)

        if disable_menu:
            self.disable_menu()

        # Create sidebar menu
        app = st.sidebar.radio(
            ' ',
            self.apps,
            format_func=lambda app: app['title'])

        # Clear session data
        if st.sidebar.button("Clear session"):
            logger.info({"message": "Clear session."})
            remove_files_by_extension(extension=".sqlite")
            st.session_state.clear()
            st.sidebar.info("Session cleared.")

        # Define unique name
        if "db_name" not in st.session_state:
            logger.info({"message": "Defining database name"})
            st.session_state.db_name = str(int(datetime.datetime.now().timestamp())) + ".sqlite"
        db = Database(file_name=st.session_state.db_name)

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

        app['function']()

    def disable_menu(self):
        logger.info({"message": "Disabling Streamlit's menu."})
        hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
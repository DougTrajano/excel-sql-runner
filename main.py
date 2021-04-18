import logging
from app.multi_app import MultiApp
from app.pages.home import home_page
from app.pages.profiling import profiling_page
from app.pages.about import about_page

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = MultiApp()
app.add_page("Home", home_page)
app.add_page("Profiling", profiling_page)
app.add_page("About", about_page)

app.run(page_title="Excel SQL Runner", disable_menu=False)
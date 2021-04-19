import logging
logging.basicConfig(level=logging.INFO)

from app.multi_app import MultiApp
from app.pages.home import home_page
from app.pages.profiling import profiling_page
from app.pages.about import about_page

app = MultiApp()
app.add_page("Home", home_page)
app.add_page("Profiling", profiling_page)
app.add_page("About", about_page)

app.run(app_title="Excel SQL Runner", disable_menu=True)
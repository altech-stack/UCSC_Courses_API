
from src.helper import Helpers, LoggerHelpers
import os

class ConfigObject():
    # Specifies API Endpoint for class search data
    api_endpoint = "https://pisa.ucsc.edu/class_search/index.php"

    # Loads default payload needed to send POST parameters to class search endpoint
    default_payload = Helpers.load_json_file(Helpers, '{}/payload.json'.format(os.getcwd()))

    # Initializes custom logging solution.. really helpful
    logger = LoggerHelpers()
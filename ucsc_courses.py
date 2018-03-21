from flask import Flask, request, jsonify, make_response
import json
import re
import requests
import os
from logger_helper import LoggerHelpers
# references:
# - restful api - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# - auth - http://flask-httpauth.readthedocs.io/en/latest/

class Helpers():
    # Function that finds the
    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def load_json_file(self, filepath):
        with open(filepath, 'rb') as f:
            json_data = json.loads(f.read())
        return json_data

class ConfigObject():
    api_endpoint = "https://pisa.ucsc.edu/class_search/index.php"
    default_payload = Helpers.load_json_file(Helpers, '{}/payload.json'.format(os.getcwd()))
    logger = LoggerHelpers()

class CourseParser():

    @staticmethod
    def group_by_heading(some_source):
        buffer = []
        for line in some_source:
            if "panel-heading-custom" in line and "H2" in line:
                if buffer: yield buffer
                buffer = [line]
            else:
                buffer.append(line)
        yield buffer

    @staticmethod
    def parse_classes_page(payload):
        raw_html_results = requests.post(ConfigObject.api_endpoint,data=payload).text

        split_raw_html_results_to_array = raw_html_results.split('\n')
        for classes in CourseParser.group_by_heading(split_raw_html_results_to_array):
            heading = classes[0]
            info = classes[1:3]
            print ("-----")
            print (heading)
            print (info)
            print("-----")
class API():
    app = Flask('ucsc_courses')

    def __init__(self):

        pass

    @staticmethod
    @app.route('/api/v1.0/open_courses', methods=['GET'])
    def open_courses():
        ConfigObject.logger.log_msg('Running the Open Courses API','INFO')
        default_payload = ConfigObject.default_payload

        # You can derive this payload using the Inspect Element feature, navigate to the Networks
        # tab, and then search for classes on https://pisa.ucsc.edu/class_search
        custom_payload = {
            "action": "results",
            "binds[:catalog_nbr_op]:": "=",
            "binds[:crse_units_op]:": "=",
            "binds[:instr_name_op]:": "=",
            "binds[:reg_status]:": "O",
            "binds[:term]:": 2182
        }

        # Combines two dictionaries together
        # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
        open_courses_payload = { **default_payload,  **custom_payload }

        results = CourseParser.parse_classes_page(open_courses_payload) 

        return jsonify({'msg': 'Success'})

    ### error handling

    @staticmethod
    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def run(self, debug=True, port=5000):
        self.app.run(port=port, debug=debug)


if __name__ == '__main__':
    app = API()
    app.run()

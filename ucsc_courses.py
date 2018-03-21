from flask import Flask, request, jsonify, make_response
import json
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


    # Parses the latest term info from the front page
    @staticmethod
    def get_term_info():
        #Gets the raw HTML results
        raw_html_results = requests.get(ConfigObject.api_endpoint).text

        # Replacement 1: Get rid of all new lines
        # Replacement 2: Every HTML comment will have a newline before it to make parsing easier
        parsed_results = str(raw_html_results.replace('\n','').replace('<!--','\n<!-- ')).split('\n')[4:]

        # Grab the string containing all the terms
        term_string = ""
        for entries in parsed_results:
            if 'term_dropdown' in entries:
                term_string = entries

        # Yes I realize that I could do this within the for loop to save runtime complexity..
        # but this is easier to read/understand for the laymen

        term_string = term_string.replace('<option value','\n<option value').split('\n')[1:]
        term_array = []

        for term in term_string:
            # Edge case: the first one has a different html tag than the rest, so we accomodate
            if 'selected' in term:
                term_id = Helpers.find_between(Helpers, term, '<option value = "', '"')
                term_value = Helpers.find_between(Helpers, term, '{}" selected="selected">'.format(term_id), '</option')
            else:
                term_id = Helpers.find_between(Helpers, term, '<option value = "', '"')
                term_value = Helpers.find_between(Helpers, term, '{}" >'.format(term_id), '</option')
            term_array.append(
                {
                    "term_id": term_id,
                    "term_value": term_value
                }
            )

        return term_array

    @staticmethod
    def parse_classes_page(payload):
        # Grabs the raw HTML page from the endpoint
        raw_html_results = requests.post(ConfigObject.api_endpoint,data=payload).text

        # Replacement 1: Get rid of all new lines
        # Notes : I saw that "panel-heading.*" are the only differentiators when parsing through the results
        # Replacement 2: Every panel-heading piece will have a newline, for easier parsing
        # Split the results by the newline that were given, and skip the first line
        parsed_results = str(raw_html_results.replace("\n","").replace\
            ('<div class="panel-heading panel-heading-custom">',
             '\n<div class="panel-heading panel-heading-custom">')).replace('<br>',' ').split("\n")[1:]


        return_data = []
        for entries in parsed_results:

            # Grab relevant data, heavily relying on html elements ( this may change a lot as the HTML page changes )
            filtered_entry = Helpers.find_between(Helpers,entries,'<div class="panel-heading panel-heading-custom"><H2 style="margin:0px;">', 'Materials</a></div>')
            filtered_json = {}
            print( filtered_entry)
            descriptive_link = Helpers.find_between(Helpers, filtered_entry, 'href = "index.php?', '"')
            class_name = Helpers.find_between(Helpers, filtered_entry, '{}">'.format(descriptive_link), '</a>')
            title = Helpers.find_between(Helpers, filtered_entry, 'title="', '"')
            link_sources = Helpers.find_between(Helpers,filtered_entry,'<img src="','"')
            class_id = Helpers.find_between(Helpers,filtered_entry,'<a id="','"').replace('class_id_','')
            instructor = Helpers.find_between(Helpers, filtered_entry, 'Instructor:</i>', '</div>')
            location = Helpers.find_between(Helpers, filtered_entry, 'Location:</i>', '</div>')
            date_time = Helpers.find_between(Helpers, filtered_entry, 'Day and Time:</i>', '</div>')
            enrolled = Helpers.find_between(Helpers, filtered_entry, '{}</div> <div class="col-xs-6 col-sm-3"> '.format(date_time), '</div')

            # Parse into JSON document
            filtered_json['status'] = title
            filtered_json['link_sources'] = link_sources
            filtered_json['class_id'] = class_id
            filtered_json['descriptive_link'] = descriptive_link
            filtered_json['class_name'] = class_name.replace('&nbsp;',' ')
            filtered_json['instructor'] = instructor
            filtered_json['location'] = location
            filtered_json['date_time'] = date_time
            filtered_json['enrolled'] = enrolled
            return_data.append(filtered_json)


        return return_data

class API():
    app = Flask('ucsc_courses')

    def __init__(self):

        pass

    @staticmethod
    @app.route('/api/v1.0/get_term_info', methods=['GET'])
    def get_all_params():

        results = CourseParser.get_term_info()

        return jsonify(results)

    @staticmethod
    @app.route('/api/v1.0/search', methods=['GET'])
    def search():
        action = request.args.get('ACTION', default="results", type=str)
        acad_career = request.args.get('acad_career', default='', type=str)
        catalog_nbr_op = request.args.get('catalog_nbr_op', default='=', type=str)
        catalog_nbr = request.args.get('catalog_nbr', default='', type=str)
        crse_units_exact = request.args.get('crse_units_exact', default='', type=str)
        crse_units_from = request.args.get('crse_units_from', default='', type=str)
        crse_units_op = request.args.get('crse_units_op', default='=', type=str)
        crse_units_to = request.args.get('crse_units_to', default='', type=str)
        days = request.args.get('days', default='', type=str)
        ge = request.args.get('ge', default='', type=str)
        instr_name_op = request.args.get('instr_name_op', default='=', type=str)
        instructor = request.args.get('instructor', default='', type=str)
        reg_status = request.args.get('reg_status', default='O', type=str)
        subject = request.args.get('subject', default='', type=str)
        term = request.args.get('term', default=CourseParser.get_term_info()[0].get('term_id'), type=str)
        times = request.args.get('times', default='', type=str)
        title = request.args.get('title', default='', type=str)

        recognized_fields = {
            "action": action,
            "acad_career": acad_career,
            "catalog_nbr_op": catalog_nbr_op,
            "catalog_nbr": catalog_nbr,
            "crse_units_exact": crse_units_exact,
            "crse_units_from": crse_units_from,
            "crse_units_op": crse_units_op,
            "crse_units_to": crse_units_to,
            "days": days,
            "ge": ge,
            "instr_name_op": instr_name_op,
            "instructor": instructor,
            "reg_status": reg_status,
            "subject": subject,
            "term": term,
            "times": times,
            "title": title
        }

        courses_injection = {
            "action": action,
            "binds[:acad_career]": acad_career,
            "binds[:catalog_nbr_op]": catalog_nbr_op,
            "binds[:catalog_nbr]": catalog_nbr,
            "binds[:crse_units_exact]": crse_units_exact,
            "binds[:crse_units_from]": crse_units_from,
            "binds[:crse_units_op]": crse_units_op,
            "binds[:crse_units_to]": crse_units_to,
            "binds[:days]": days,
            "binds[:ge]": ge,
            "binds[:instr_name_op]": instr_name_op,
            "binds[:instructor]": instructor,
            "binds[:reg_status]": reg_status,
            "binds[:subject]": subject.upper(),
            "binds[:term]": term,
            "binds[:times]": times,
            "binds[:title]": title
        }
        results = CourseParser.parse_classes_page(courses_injection)

        return_payload = {
            'recognized_fields': recognized_fields,
            'payload': results
        }

        return jsonify(return_payload)

    @staticmethod
    @app.route('/api/v1.0/open_courses', methods=['GET'])
    def open_courses():
        ConfigObject.logger.log_msg('Running the Open Courses API','INFO')
        default_payload = ConfigObject.default_payload

        # You can derive this payload using the Inspect Element feature, navigate to the Networks
        # tab, and then search for classes on https://pisa.ucsc.edu/class_search


        custom_payload = {
            "binds[:catalog_nbr_op]:": "=",
            "binds[:crse_units_op]:": "=",
            "binds[:instr_name_op]:": "=",
            "binds[:reg_status]:": "O",
            "binds[:term]:": CourseParser.get_term_info()[0].get('term_id')
        }

        # Combines two dictionaries together
        # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
        open_courses_payload = { **default_payload,  **custom_payload }

        results = CourseParser.parse_classes_page(open_courses_payload)

        return jsonify(results)


    @staticmethod
    @app.route('/api/v1.0/open_courses/<int:num_of_results>', methods=['GET'])
    def open_courses_num(num_of_results):
        ConfigObject.logger.log_msg('Running the Open Courses API', 'INFO')
        default_payload = ConfigObject.default_payload

        # You can derive this payload using the Inspect Element feature, navigate to the Networks
        # tab, and then search for classes on https://pisa.ucsc.edu/class_search
        custom_payload = {
            "action": "update_segment",
            "binds[:catalog_nbr_op]:": "=",
            "binds[:crse_units_op]:": "=",
            "binds[:instr_name_op]:": "=",
            "binds[:reg_status]:": "O",
            "binds[:term]:": 2182,
            "rec_dur":num_of_results
        }

        # Combines two dictionaries together
        # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression

        open_courses_payload = {**default_payload, **custom_payload}

        results = CourseParser.parse_classes_page(open_courses_payload)

        return jsonify(results)

    @staticmethod
    @app.route('/api/v1.0/courses/<string:status>', methods=['GET'])
    def courses(status):
        ConfigObject.logger.log_msg('Running the Open Courses API', 'INFO')
        default_payload = ConfigObject.default_payload

        # You can derive this payload using the Inspect Element feature, navigate to the Networks
        # tab, and then search for classes on https://pisa.ucsc.edu/class_search
        reg_status = "O"
        if 'open' in status.lower():
            reg_status = "O"
        elif 'all' in status.lower():
            reg_status = "all"
        else:
            return jsonify({
                'msg': 'Your only choices in this endpoint is /open or /all, otherwise, just use /open_courses'
            })

        print(CourseParser.get_term_info()[0])
        custom_payload = {
            "binds[:catalog_nbr_op]:": "=",
            "binds[:crse_units_op]:": "=",
            "binds[:instr_name_op]:": "=",
            "binds[:reg_status]:": str(reg_status),
            "binds[:term]:": CourseParser.get_term_info()[0].get('term_id')
        }

        # Combines two dictionaries together
        # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
        open_courses_payload = {**default_payload, **custom_payload}

        results = CourseParser.parse_classes_page(open_courses_payload)

        return jsonify(results)

    @staticmethod
    @app.route('/api/v1.0/courses/<string:status>/<int:num_of_results>', methods=['GET'])
    def courses_num(status, num_of_results):
        ConfigObject.logger.log_msg('Running the Open Courses API', 'INFO')
        default_payload = ConfigObject.default_payload

        # You can derive this payload using the Inspect Element feature, navigate to the Networks
        # tab, and then search for classes on https://pisa.ucsc.edu/class_search
        reg_status = "O"
        if 'open' in status.lower():
            reg_status = "O"
        elif 'all' in status.lower():
            reg_status = "all"
        else:
            return jsonify({
                'msg': 'Your only choices in this endpoint is /open or /all, otherwise, just use /open_courses'
            })

        custom_payload = {
            "action": "update_segment",
            "binds[:catalog_nbr_op]:": "=",
            "binds[:crse_units_op]:": "=",
            "binds[:instr_name_op]:": "=",
            "binds[:reg_status]:": str(reg_status),
            "binds[:term]:": CourseParser.get_term_info()[0].get('term_id'),
            "rec_dur": num_of_results
        }

        # Combines two dictionaries together
        # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
        open_courses_payload = {**default_payload, **custom_payload}

        # Parse resulting payload into the results object
        results = CourseParser.parse_classes_page(open_courses_payload)

        return jsonify(results)

    ### error handling

    @staticmethod
    @app.errorhandler(404)
    def not_found(error):
        return   make_response(jsonify({'error': 'Not found'}), 404)

    def run(self, debug=True, port=5000):
        self.app.run(port=port, debug=debug)


if __name__ == '__main__':
    app = API()
    app.run()

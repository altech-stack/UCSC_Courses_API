from flask import Flask, request, jsonify, make_response
import requests
from src.course_parser import CourseParser
from ucsc_courses import app
from src.config import ConfigObject

@app.route('/api/v1.0/get_term_info', methods=['GET'])
def get_all_params():

    results = CourseParser.get_term_info()

    return jsonify(results)

@app.route('/api/v1.0/search', methods=['GET'])
def search():

    # See: https://stackoverflow.com/a/46321103 for reading uri queries and assigning default values
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
        "binds[:title]": title,
        "rec_dur":int(request.args.get('count', 100))
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
        "binds[:term]:": 2210,
        "rec_dur":num_of_results
    }

    # Combines two dictionaries together
    # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression

    open_courses_payload = {**default_payload, **custom_payload}

    results = CourseParser.parse_classes_page(open_courses_payload)

    return jsonify(results)

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
    
    bind_term = request.args.get('term', default=CourseParser.get_term_info()[0].get('term_id'), type=str)
    custom_payload = {
        "action": "update_segment",
        "binds[:catalog_nbr_op]:": "=",
        "binds[:crse_units_op]:": "=",
        "binds[:instr_name_op]:": "=",
        "binds[:reg_status]:": str(reg_status),
        "binds[:term]:":bind_term,
        "rec_dur": num_of_results
    }

    # Combines two dictionaries together
    # See: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
    open_courses_payload = {**default_payload, **custom_payload}

    # Parse resulting payload into the results object
    results = CourseParser.parse_classes_page(open_courses_payload)

    return jsonify(results)

### error handling

@app.errorhandler(404)
def not_found(error):
    return   make_response(jsonify({'error': 'Not found'}), 404)

def run(self, debug=True, port=5000):
    self.app.run(port=port, debug=debug)
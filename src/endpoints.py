from flask import Flask, request, jsonify, make_response
import requests
from src.course_parser import CourseParser
from ucsc_courses import app
from src.config import ConfigObject

@app.route('/api/terms', methods=['GET'])
def get_all_params():
    results = CourseParser.get_term_info()
    return jsonify(results)

@app.route('/api/search', methods=['GET'])
def search():
    query = CourseParser.parse_request(request)
    results = CourseParser.parse_classes_page(query)

    return_payload = {
        'recognized_fields': query,
        'payload': results
    }

    return jsonify(return_payload)


@app.route('/api/courses', methods=['GET'])
def courses():
    ConfigObject.logger.log_msg('Running the Open Courses API', 'INFO')
    default_payload = ConfigObject.default_payload

    # You can derive this payload using the Inspect Element feature, navigate to the Networks
    # tab, and then search for classes on https://pisa.ucsc.edu/class_search
    print(CourseParser.get_term_info()[0])
    custom_payload = {
        "binds[:term]:": CourseParser.get_term_info()[0].get('term_id'),
        "binds[:subject]": request.args.get('subject', '').upper(),
        "binds[:reg_status]": request.args.get('reg_status', 'all'),
        "rec_dur": request.args.get('count', 25),
        'type': request.args.get('type', 'all')
    }
    courses_payload = {**default_payload, **custom_payload}

    results = CourseParser.parse_classes_page(courses_payload)

    return jsonify({'payload':results, 'query':custom_payload})

@app.route('/api/courses/<string:subject>', methods=['GET'])
def get_subject(subject):
    ConfigObject.logger.log_msg(f'Query for all {subject} courses', 'INFO')
    default_payload = ConfigObject.default_payload

    # You can derive this payload using the Inspect Element feature, navigate to the Networks
    # tab, and then search for classes on https://pisa.ucsc.edu/class_search
    print(CourseParser.get_term_info()[0])
    custom_payload = {
        "binds[:term]:": CourseParser.get_term_info()[0].get('term_id'),
        "binds[:subject]": subject.upper(),
        "binds[:reg_status]": request.args.get('reg_status', 'all'),
        "rec_dur": request.args.get('count', 25),
        'type': request.args.get('type', 'all')
    }
    courses_payload = {**default_payload, **custom_payload}

    results = CourseParser.parse_classes_page(courses_payload)

    return jsonify({'payload':results, 'query':custom_payload})

@app.route('/api/course/<string:course>', methods=['GET'])
def find_course(course):
    print(CourseParser.get_term_info()[0])
    nums = [str(i) for i in range(1, 11)]
    subject_len = 3 if course[3] in nums else 4
    custom_payload = {
        "binds[:catalog_nbr]:": course[subject_len:],
        "binds[:crse_units_op]:": "=",
        "binds[:instr_name_op]:": "=",
        "binds[:reg_status]:": 'all',
        "binds[:subject]":course[:subject_len].upper(),
        "binds[:term]:": CourseParser.get_term_info()[0].get('term_id')
    }

    courses_payload = {**ConfigObject.default_payload, **custom_payload}

    results = CourseParser.parse_classes_page(courses_payload)

    return jsonify({'payload':results, 'query':custom_payload})

### error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

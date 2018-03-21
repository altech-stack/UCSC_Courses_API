# UCSC Courses API

A small ongoing project to get students started in API development using flask. Students from UCSC are encouraged to fork it and make any additions they want to enhance the API experience (within reason, and through the appropriate channels)


## Getting Started

First, fork the repo and then clone it from your repository.


### Prerequisites

The codebase is written in Python 3.6. Make sure your workstation has python 3.6 installed.

Below is what I would do to make sure you're in a good spot.

```
cd /path/to/folder
virtualenv --no-site-packages -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Requirements.txt should contain all of the libraries needed (there's not much) for this project.

## How to run

You can run by performing the command:
```
python ucsc_courses.py
```

By default, the API server runs on port 5000. You can view a sample endpoint below: 
```
http://localhost:5000/api/v1.0/courses/all

```
And you will receive (redacted) the following sample JSON:

```
[
  {
    "class_id": "70933", 
    "class_name": "ACEN 110A - 02   Adv Acad English 1", 
    "date_time": " TBA To Be Arranged", 
    "descriptive_link": "action=detail&amp;class_data=YToyOntzOjU6IjpTVFJNIjtzOjQ6IjIxODQiO3M6MTA6IjpDTEFTU19OQlIiO3M6NToiNzA5MzMiO30%3D", 
    "enrolled": "0 of 0 Enrolled", 
    "instructor": " Staff", 
    "link_sources": "https://pisa.ucsc.edu/cs9/prd/images/PS_CS_STATUS_CLOSED_ICN_1.gif", 
    "location": " LEC: Humanities 1 110", 
    "status": "Closed"
  } 
]
```



## Available Endpoints to Play Around With

There are a few endpoints available for students to play around with.

```
GET /api/v1.0/get_term_info' # Gets all available term info
GET /api/v1.0/search' # Uses URL Parameters after search to perform custom searches
# Example: http://localhost:5000/api/v1.0/search?subject=cmps&reg_status=all&term=2180
GET /api/v1.0/open_courses' # Gets all open courses for the latest term
GET /api/v1.0/open_courses/<int:num_of_results>' # Gets all open courses + overriding the default 25 search results
# Example: http://localhost:5000/api/v1.0/open_courses/50
GET /api/v1.0/courses/<string:status>' # Gets all courses, open/closed
# Example: http://localhost:5000/api/v1.0/courses/all
GET /api/v1.0/courses/<string:status>/<int:num_of_results>' #Gets all courses, open/closed, and number of results
# Example: http://localhost:5000/api/v1.0/courses/all/50
```

## Libraries used

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Requests](http://docs.python-requests.org/en/master/) - Library to call GET/POST requests


## Contributing

To contribute, fork the repo, make your changes, and submit Pull requests to this repo. I or other contributors will review and will approve if it doesn't break and is appropriate (no redundant endpoints, no redundant code, etc). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



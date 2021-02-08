# UCSC Courses API

A small ongoing project to get students started in API development using flask. Students from UCSC are encouraged to fork it and make any additions they want to enhance the API experience (within reason, and through the appropriate channels)


## Getting Started

First, fork the repo and then clone it from your repository.


### Prerequisites

The codebase is written in Python 3.6. Make sure your workstation has python 3.6 installed.

Requirements.txt should contain all of the libraries needed (there's not much) for this project.

## How to run

You can run by performing the command:
```
python ucsc_courses.py
```



By default, the API server runs on port 5000. You can view a sample endpoint below: 
```
http://localhost:5000/api/courses

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

Or, you can run a bash command:
```
curl http://localhost:5000/api/courses
```

## Applications

- Let's say you have an iOS/Android/Web client for UCSC class search results. Instead of parsing it on the client side (and having the user deal with all the heavy lifting), you can put this python file on a server and run it there instead. There's also a predictable schema in JSON form so that the client will always expect the same JSON structure per request. If there are any problems to the HTML, you can modify the parsing functions and then return the same JSON structure. 
- Let's say you have a database and you have another script that runs in a cron job that queries this server every 10 seconds. Have the script write the results to a database and now you can perform time based analytics. With the ability to store time based data, you can answer questions like "How fast did this class fill up", or "What is the likelihood for class X,Y,Z to fill up during a particular quarter". 

## Available Endpoints to Play Around With

There are a few endpoints available for students to play around with. Checkout src/endpoints.py to see all of the endpoints for this project. It lacks a description, but those are all of the endpoints

```
GET /api/terms' # Gets all available term info
 
GET /api/search' # Uses URL Parameters after search to perform custom searches
# Example: http://localhost:5000/api/search?subject=cmps&reg_status=all&term=2180
 
# Example: http://localhost:5000/api/courses?reg_status=open
 
GET /api/courses/<string:status>' # Gets all courses, open/closed
# Example: http://localhost:5000/api/courses
 
GET /api/courses?count=50&reg_status=open' #Gets all courses, open/closed, and number of results
# Example: http://localhost:5000/api/courses?count=50

GET /api/courses/<subject>' #Gets courses for this specific subject (specify open, closed, upper, lower, grad in the data)
# Example: http://localhost:5000/api/courses/cse?type=upper&count=100

GET /api/course/<course_num>' #Gets all courses, open/closed, and number of results
# Example: http://localhost:5000/api/course/cse101


EXAMPLE:
http://localhost:5000/api/courses/cse?count=1
{
  "payload": [
    {
      "class_id": "44438", 
      "class_name": "CSE 3 - 01   Personal Computers", 
      "date_time": "TuTh 11:40AM-01:15PM", 
      "descriptive_link": "action=detail&amp;class_data=YToyOntzOjU6IjpTVFJNIjtzOjQ6IjIyMTAiO3M6MTA6IjpDTEFTU19OQlIiO3M6NToiNDQ0MzgiO30%3D", 
      "enrolled": "349 of 400 ", 
      "instructor": " Moulds,G.B.", 
      "link_sources": "https://pisa.ucsc.edu/cs9/prd/images/PS_CS_STATUS_OPEN_ICN_1.gif", 
      "location": " LEC: Remote Instruction", 
      "status": "Open"
    }
  ], 
  "query": {
    "binds[:reg_status]": "all", 
    "binds[:subject]": "CSE", 
    "binds[:term]:": "2210", 
    "rec_dur": "1", 
    "type": "all"
  }
}
```

## Future Work

- Additional endpoints - Maybe an endpoint to search by teacher, or get a certain class across all terms, etc. 
- Ongoing HTML parsing - UCSC's going to change their site all the time. One of the benefits of having a server is that if you have clients that depend on this type of data, you only need to change the server to fix the parsing, and leave the schema as is. 
- Improvements to the /search api. Honestly I did this one really quick because I wanted to show how to take in uri queries and embed them into a request. 
- Get more class information - I actually saved the underlying class links in the payload, which can be used to do another GET request to get stuff like discussion classes, description, etc. Didn't have time for V1, but will definitely explore later.


## Libraries Used

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Requests](http://docs.python-requests.org/en/master/) - Library to call GET/POST requests


## Contributing

To contribute, fork the repo, make your changes, and submit Pull requests to this repo. I or other contributors will review and will approve if it doesn't break and is appropriate (no redundant endpoints, no redundant code, etc). 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details



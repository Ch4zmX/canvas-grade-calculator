import requests
from dotenv import load_dotenv
load_dotenv()
import os

CANVAS = "https://canvas.ucsc.edu"
API_KEY = os.getenv('TOKEN')

def keyIsValid(key): # checks if the API key is valid
    json = requests.get(CANVAS + "/api/v1/courses", 
                        headers={'Authorization': 'Bearer ' + key}).json()
    if "errors" in json: # the json will contain an error if key invalid
        return False
    return True

def getUserCoursesJSON(count = 10):
    json = requests.get(CANVAS + "/api/v1/courses", 
                        params={'per_page': count},
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    #print(CANVAS + "/api/v1/courses")
    return json

def getCourseAssignmentJSON(course_id, assignment_id):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/assignments/{assignment_id}", 
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    return json

def getCourseAssignmentsJSON(course_id, ids: list = [], count = 100):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/assignments", 
                        params={'per_page': count, 'assignment_ids[]': ids},
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    return json

def getUserGradesJSON(course_id, count = 100):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/students/submissions", 
                        params={'per_page': count},
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    return json

def getUserGradeJSON(course_id, assignment_id, count = 100):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/students/submissions", 
                        params={'per_page': count, 'assignment_ids[]': assignment_id},
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    return json

def getAssignmentWeightsJSON(course_id, count = 100):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/assignment_groups", 
                        params={'per_page': count}, 
                        headers={'Authorization': 'Bearer ' + API_KEY}).json()
    return json

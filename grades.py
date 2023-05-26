import os
import requests
from dotenv import load_dotenv
load_dotenv()

CANVAS = "https://canvas.ucsc.edu"
API_KEY = os.getenv('TOKEN')

def key_is_valid(key): # This function checks if the API key is valid
    json = requests.get(CANVAS + "/api/v1/courses",
                        headers={'Authorization': 'Bearer ' + key}).json()
    if "errors" in json: # the json will contain an error if key invalid
        return False
    return True

# Get a Canvas API token from canvas settings
# No need to store password, will allow direct access to grades



def get_courses():


    json = requests.get(CANVAS + "/api/v1/courses",
                       headers={'Authorization': 'Bearer '+API_KEY}).json()
    courses = {}
    for course in json:
        courses[course['id']] = course['name']

    return courses

def get_grades(course_id):
    json = requests.get(CANVAS + f"/api/v1/courses/{course_id}/students/submissions", 
                        headers={'Authorization': 'Bearer '+API_KEY}).json()
    return json

if __name__ == '__main__':

    if not key_is_valid(API_KEY):
        while not key_is_valid(API_KEY):
            print("API Key is invalid!")
            API_KEY = input("Enter your Canvas API Key: ").strip()

        with open(".env", "w") as f:
            os.putenv("TOKEN", API_KEY)
        print("API Key is valid! Continuing...")

    courses = get_courses()
    course_ids = {}
    print("Courses Found: ")
    for i, course_id in enumerate(courses.keys()):
        print(f" {i:<5}Class Name: {courses[course_id]:<50}ID: {course_id}")
        course_ids[i] = course_id
    i = int(input("Enter the number corresponding to your class: "))

    grades = get_grades(course_id=course_ids[i])
    print(grades)
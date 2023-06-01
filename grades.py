import canvas
import os

def storeKey(key: str):
    if not canvas.keyIsValid(key): # if the key is invalid, ask for a new one, and save it into env to store
            while not canvas.keyIsValid(key):
                print("API Key is invalid!")
                key = input("Enter your Canvas API Key: ").strip()

            with open(".env", "w") as f:
                os.putenv("TOKEN", key)
    print("API Key is valid! Continuing...")

def print_grades(grades: dict[dict]):  

    print(f'{"":<8}{"Assignment":<78}{"Grade":<25}{"Category":<50}{"Weight":<50}')
    for grade in grades.keys():
        id = grade
        grade = grades[grade]
        print(f"{id}: {grade['name'][:75]+('...' if len(grade['name']) > 75 else ''):<78}{grade['score']}/{grade['points']:<25}{grade['weight_group']:<50}{grade['weight']}")

if __name__ == '__main__':

    storeKey(canvas.API_KEY)
    print("User Courses Found: ")
    json = list(canvas.getUserCoursesJSON(100))
    for i, course in enumerate(json):
        if 'name' in course:
            print(f"{str(i)+':':<3} {course['id']} - {course['name']}")
            
    
    course = json[int(input("Enter the index number corresponding to your class (e.g 1): "))]
    course_id, course_name = course['id'], course['name']

    weighted = bool(course['apply_assignment_group_weights'])
    print("Course is weighted:", weighted)
    print(f"\nGetting grades for {course['name']}...\n")

    gradesJSON = canvas.getUserGradesJSON(course_id)
    assignment_ids = []
    grades = {}

    for grade in gradesJSON: # Initial loop to get all assignment ids, now we can just pass in a list of these ids to get only the assignments we want
        #assignment_ids.append(grade['assignment_id'])
        if 'score' not in grade or grade['score'] is None:
            grades[grade['assignment_id']] = {'score': '--'}
            continue
        grades[grade['assignment_id']] = {'score': grade['score']}

    assignmentsJSON = canvas.getCourseAssignmentsJSON(course_id=course_id)

    weights = {}
    weightsJSON = canvas.getAssignmentWeightsJSON(course_id=course_id)

    for weight in weightsJSON:
        weights[weight['id']] = {'name': weight['name'], 'weight': weight['group_weight'] if weighted else 1}

    for assignment in assignmentsJSON:
        weight_id = assignment['assignment_group_id']

        if assignment['points_possible'] is None:
            points = '--'
        else:
            points = assignment['points_possible']
        grades[assignment['id']]['points'] = points
        grades[assignment['id']]['name'] = assignment['name']
        grades[assignment['id']]['weight_group'] = weights[weight_id]['name']
        grades[assignment['id']]['weight'] = weights[weight_id]['weight']

    print_grades(grades)
    #print(weights)
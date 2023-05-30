import canvas

def storeKey(key: str):
    if not canvas.keyIsValid(key): # if the key is invalid, ask for a new one, and save it into env to store
            while not canvas.keyIsValid(key):
                print("API Key is invalid!")
                key = input("Enter your Canvas API Key: ").strip()

            with open(".env", "w") as f:
                os.putenv("TOKEN", key)
    print("API Key is valid! Continuing...")

def print_grades(grades: dict[dict]):  

    print(f'{"Assignment":<78}{"Grade":<25}{"Category":<50}{"Weight":<50}')
    for grade in grades.keys():
        grade = grades[grade]
        print(f"{grade['name'][:75]+('...' if len(grade['name']) > 75 else ''):<78}{grade['score']}/{grade['points']:<25}{grade['weight_group']:<50}{grade['weight']}")

if __name__ == '__main__':

    storeKey(canvas.API_KEY)
    print("User Courses Found: ")
    for i, course in enumerate(json := canvas.getUserCoursesJSON(100)):
        if 'name' in course:
            print(f"{str(i)+':':<3} {course['id']} - {course['name']}")
    json = list(json)
    course = json[int(input("Enter the index number corresponding to your class (e.g 1): "))]

    print(f"\nGetting grades for {course['name']}...\n")

    assignmentsJSON, assignments = canvas.getCourseAssignmentsJSON(course['id']), {}
    for assignment in assignmentsJSON: # store assignment name and points possible in a dictionary
        weightsJSON = canvas.getAssignmentWeightJSON(course['id'], assignment['assignment_group_id'])
        points = assignment['points_possible'] or '--'
        assignments[assignment['id']] = {'assignment_id': assignment['id'], 'name': assignment['name'], 'points': points, 'weight_group': weightsJSON['name'], 'weight': weightsJSON['group_weight']}
    gradesJSON = canvas.getUserGradeJSON(course['id'], assignments.keys())

    for grade in gradesJSON: # print out and store the grade for each assignment
        assignment_id = grade['assignment_id']
        assignments[assignment_id]['score'] = grade['score'] or '--'

    print_grades(assignments)
    #print(weights)
import canvas

def storeKey(key):
    if not canvas.keyIsValid(key): # if the key is invalid, ask for a new one, and save it into env to store
            while not canvas.keyIsValid(key):
                print("API Key is invalid!")
                key = input("Enter your Canvas API Key: ").strip()

            with open(".env", "w") as f:
                os.putenv("TOKEN", key)
    print("API Key is valid! Continuing...")

if __name__ == '__main__':

    storeKey(canvas.API_KEY)
    print("User Courses Found: ")
    for i, course in enumerate(json := canvas.getUserCoursesJSON(100)):
        if 'name' in course:
            print(f"{str(i)+':':<3} {course['id']} - {course['name']}")
    json = list(json)
    course = json[int(input("Enter the index number corresponding to your class (e.g 1): "))]

    print(f"\nGetting grades for {course['name']}...\n")

    json, assignments = canvas.getCourseAssignmentsJSON(course['id']), {}
    for assignment in json: # store assignment name and points possible in a dictionary
        assignments[assignment['id']] = assignment['name'], assignment['points_possible']
    gradesJSON = canvas.getUserGradeJSON(course['id'], assignments.keys())
    weights = {}
    
    for assignment_id in assignments.keys(): # store assignment name and points possible in a dictionary
        weightsJSON = canvas.getAssignmentWeightJSON(course['id'], assignment_id)
        weights[assignment_id] =  weightsJSON['name'], weightsJSON['group_weight']
    grades = {}
    for grade in gradesJSON: # print out and store the grade for each assignment
        assignment_id = grade['assignment_id']
        grades[assignments[assignment_id][0]] = grade['score'], assignments[assignment_id][1], weights[assignment_id][1]
        print(f"{assignments[grade['assignment_id']][0]}: {grade['score']} / {assignments[grade['assignment_id']][1]}")
    print(grades)
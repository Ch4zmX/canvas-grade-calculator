import canvas



print(grades)


assignmentsJSON, assignments = canvas.getCourseAssignmentsJSON(59481), {}
for assignment in assignmentsJSON: # store assignment name and points possible in a dictionary
    weightsJSON = canvas.getAssignmentWeightJSON(59481, assignment['assignment_group_id'])
    if (points := assignment['points_possible']) is None:
        points = '--'
    assignments[assignment['id']] = {'assignment_id': assignment['id'], 'name': assignment['name'], 'points': points, 'weight_group': weightsJSON['name'], 'weight': weightsJSON['group_weight']}
gradesJSON = canvas.getUserGradeJSON(59481, assignments.keys())

for grade in gradesJSON: # print out and store the grade for each assignment
    print(grade)
    assignment_id = grade['assignment_id']

    if 'score' in grade: # Check for edge case if assignment doesnt have a grade
        if grade['score'] is None:
            assignments[assignment_id]['score'] = '--'
        else:
            assignments[assignment_id]['score'] = grade['score']
    else:
        assignments[assignment_id]['score'] = '--'
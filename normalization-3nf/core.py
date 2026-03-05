import nbformat as nbf

### Functional Dependencies ###

INTRO = """
## Database Normalization in Z3

In the previous notebook, we wrote some functions to help us represent and check for functional dependencies.
In this notebook, we will expand upon this to write functions to determine if a relation satisfies 2NF and 3NF.

The relations we will test are below:

$$ R_1(\\underline{studentID}, \\underline{courseID}, studentName, courseFee) $$

$$ R_2(\\underline{enrollmentID}, studentId, studentName, courseID, courseName) $$

Just as before, the first thing we must do is determine the functional dependencies in the relation.
"""

RELATIONS = """
In order to represent functional dependencies in Z3, we first need to create variables to represent two rows in the relation.
In the code below, we have created one variable for each attribute, for two arbitrary rows 'A' and 'B'.

No code is needed for this cell, **simply run the cell to create the variables**.
"""

RELATIONS_CODE = """
# Create variables to represent two arbitrary rows in the relation
row1 = {
    'studentID' : String('A.studentID'),
    'courseID' : String('A.courseID'),
    'studentName' : String('A.studentName'),
    'courseFee' : String('A.courseFee'),
}
row2 = {
    'studentID' : String('B.studentID'),
    'courseID' : String('B.courseID'),
    'studentName' : String('B.studentName'),
    'courseFee' : String('B.courseFee'),
}
"""

DEPENDENCIES = """
### Functional Dependencies

Let's take a look at the first relation:

$$ R_1(\\underline{studentID}, \\underline{courseID}, studentName, courseFee) $$

Which has functional dependencies:

$$ studentID \\rightarrow studentName $$
$$ courseID \\rightarrow courseFee $$

In the previous notebook, you created functions to encode and check for functional dependencies. 
These functions are provided below.

**Complete the code below** to create the functional dependencies for R1.
"""

DEPENDENCIES_CODE = """
# These functions should be imported from another file
def functional_dependency(X, Y):
    return Implies( row1.X == row2.X, row1.Y == row2.Y ) 

def has_fd(s, X, Y):
    s.push()

    s.add(
        And( row1.X == row2.X, row1.Y != row2.Y )
    )

    result = s.check() == unsat # If we can't find a counterexample, then X -> Y

    # Remove the most recent constraint
    s.pop()

    return result

# Initialize solver
s = Solver()

# Add the functional dependencies
s.add( functional_dependency( ) ) # REPLACE THIS LINE
s.add( functional_dependency( ) ) # REPLACE THIS LINE
    
# The following code should ouput True for both
print("studentID -> studentName :", has_fd(s, "studentID", "studentName"))
print("courseID -> courseName :", has_fd(s, "courseID", "courseName"))
"""

SECOND_NF = """
Now that we are able to represent functional dependencies, we can write a function to determine if a relation is in 2NF!

Recall that a relation is in 2NF if no partial dependencies exist. 
That is, every attribute that is not in the primary key must depend on *every* attribute in the primary key.

In order to prove whether or not the relation is normalized, we must check that studentName and courseFee depend on *both* studentID and courseID.
**Complete the code below** to finish the function that determines if the relation is in 2NF
"""

SECOND_NF_CODE = """
def is_2nf(s, primary_key, non_prime)
    # Check that each non-prime attribute depends on the entire primary key
    for attribute in non_prime_attributes:
        for key in primary_key:
            dependency_exists = False # REPLACE THIS LINE

            if not dependency_exists:
                print("The relation has a partial dependency.", attribute, "does not depend on key attribute", key)
                return False
    return True

# Determine the primary key
primary_key = ['studentID', 'courseID']
non_prime_attributes = ['studentName', 'courseFee']

# Initialize solver
s = Solver()

# Create the functional dependencies:
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES

# Should output False
print("Is R1 in 2NF?", is_2nf(s, primary_key, non_prime_attributes))
"""

SECOND_NF_OUTRO ="""
Great! We have now proven the relation is not normalized, because studentName does not does not depend on courseID.
Additionally, courseName does not depend on studentID!
"""

THIRD_NF_INTRO = """
### Determining 3NF

Next, let's try to prove whether a function is in third normal form.

Here is our next relation:

$$ R_2(\\underline{enrollmentID}, studentId, studentName, courseID, courseName) $$

With the following functional dependencies:

$$ enrollmentID \\rightarrow studentID $$
$$ enrollmentID \\rightarrow studentName $$
$$ studentID \\rightarrow studentName $$
$$ enrollmentID \\rightarrow courseID $$
$$ enrollmentID \\rightarrow courseName $$
$$ courseID \\rightarrow courseName $$
"""

THIRD_NF_2NF = """
Recall that in order for a function to satisfy 3NF, it must already satisfy 2NF.

**Complete the code below** to determine if the relation is in 2NF
"""

THIRD_NF_2NF_CODE = """
# Create variables to represent two arbitrary rows in the relation
row1 = {
    'enrollmentID' : String('A.enrollmentID'),
    'studentID' : String('A.studentID'),
    'studentName' : String('A.studentName'),
    'courseID' : String('A.courseID'),
    'courseName' : String('A.courseName'),
}
row2 = {
    'enrollmentID' : String('B.enrollmentID'),
    'studentID' : String('B.studentID'),
    'studentName' : String('B.studentName'),
    'courseID' : String('B.courseID'),
    'courseName' : String('B.courseName'),
}

# Determine the primary key
primary_key = ['enrollmentID']
non_prime_attributes = ['studentID', 'studentName', 'courseID', 'courseName']

# Initialize solver
s = Solver()

# Create the functional dependencies:
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES
s.add( False ) # REPLACE THESE LINES

print("Does the relation satisfy 2NF:", check_2nf(s, primary_key, non_prime_attributes))
"""

THIRD_NF = '''
Great! Now all that's left is to prove whether or not the relation satisfies 3NF.

Recall that a relation satisfies 3NF if there are no transitive dependencies. 
Transitive dependencies are function dependencies of the form:

$$ X \\rightarrow Y $$
$$ Y \\rightarrow Z $$

In other words, every non-prime attribute should depend only on the primary key. 
If any non-prime attribute depends on another non-prime attribute, the relation is not in 3NF.

**Complete the code below** to finish the function so that it returns true if the given relation satisfies 3NF.
Your function should return False for the example relation.
'''

THIRD_NF_CODE = '''
def check_3nf(s, primary_key, non_prime_attributes):
    # Check that the relation is in 2NF
    if True: # REPLACE THIS LINE
        return False

    # Check all pairs of non-prime attributes for transitive dependencies
    for attribute1 in non_prime_attributes:
        for attribute2 in non_prime_attributes:
            if True: # REPLACE THESE LINES
                return

print("Relation satisfies 3NF:", check_3nf(s, non_prime_attributes))
'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_markdown_cell(RELATIONS),
                       nbf.v4.new_code_cell(RELATIONS_CODE),
                       nbf.v4.new_markdown_cell(DEPENDENCIES),
                       nbf.v4.new_code_cell(DEPENDENCIES_CODE),
                       nbf.v4.new_markdown_cell(SECOND_NF),
                       nbf.v4.new_code_cell(SECOND_NF_CODE),
                       nbf.v4.new_markdown_cell(SECOND_NF_OUTRO),
                       nbf.v4.new_markdown_cell(THIRD_NF_INTRO),
                       nbf.v4.new_markdown_cell(THIRD_NF_2NF),
                       nbf.v4.new_code_cell(THIRD_NF_2NF_CODE),
                       nbf.v4.new_markdown_cell(THIRD_NF),
                       nbf.v4.new_code_cell(THIRD_NF_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "normalization-3nf/NORMALIZATION-3NF-CORE.ipynb" )
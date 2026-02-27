import nbformat as nbf

### Functional Dependencies ###

INTRO = """
## Database Normalization in Z3

In the previous notebook, we wrote some functions to help us determine if a relation satisfies 2NF. 
In this notebook, we will expand upon this to write a function to determine if a relation satisfies 3NF.

The relation we will test is below:

$$ R_1(\\underline{enrollmentID}, studentId, studentName, courseID, courseName) $$

Just as before, the first thing we must do is determine the functional dependencies in the relation.
"""

DEPENDENCIES = """
### Encoding Functional Dependencies

For two attributes X and Y, we say that X determines Y, $ X \\rightarrow Y $, if for any two rows in the relation:

$$ row1.X = row2.X \\rightarrow row1.Y = row2.Y $$

In other words, each value of X uniquely determines a value for Y.

**Complete the code below** to create a function that encodes a functional dependendency in Z3.
"""

DEPENDENCIES_CODE = """
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

def functional_dependency(X, Y):
    return Implies( False ) # REPLACE THIS LINE    

# Initialize solver
s = Solver()

# Add two functional dependencies
s.add( functional_dependency('enrollmentID', 'studentID') )
s.add( functional_dependency('enrollmentID', 'courseName') )
    
showSolver(s)
"""

CHECK_FOR_DEPENDENCY = """
Great! Next, to determine if a relation is normalized, we must check whether or not certain dependencies exist.

We can do this by adding the following constraint:

$$ row1.X = row2.X \land row1.Y \\neq row2.Y $$

Here, you can see we are asking the solver to find a case where the two rows share the same value of X, but they do not have the same value for Y. 
This would mean there is a counterexample where X does not determine Y. If no such counterexample exists, then we have proven the functional dependency exists.

**Complete the code below** to create a function that tests whether or not a functional dependency exists.
"""

CHECK_FOR_DEPENDENCY_CODE = """
def has_fd(s, X, Y):
    s.push()

    s.add(
        And( False ) # REPLACE THIS LINE
    )

    result = s.check() == unsat # If we can't find a counterexample, then X -> Y

    # Remove the most recent constraint
    s.pop()

    return result

# Initialize solver
s = Solver()

# Add a functional dependency
s.add( functional_dependency('enrollmentID', 'studentID') )

# Check if the FD exists:
print("enrollmentID -> studentID :", has_fd(s, 'enrollmentID', 'studentID'))

# Check for a non-existent FD:
print("studentID -> courseName :", has_fd(s, 'studentID', 'courseName'))
"""

SECOND_NF = """
### Determining 2NF

Now that we are able to represent functional dependencies, we can write a function to determine if a relation is in 3NF!

Recall that in order for a relation to satisfy 3NF it must first satisfy 2NF. 
In the previous notebook, we already wrote a function to do this, which has been provided here.

Let's take a look at the example again:

$$ R_1(\\underline{enrollmentID}, studentId, studentName, courseID, courseName) $$

With the following functional dependencies:

$$ enrollmentID \\rightarrow studentID $$
$$ enrollmentID \\rightarrow studentName $$
$$ studentID \\rightarrow studentName $$
$$ enrollmentID \\rightarrow courseID $$
$$ enrollmentID \\rightarrow courseName $$
$$ courseID \\rightarrow courseName $$

**Complete the code below** to determine if the relation is in 2NF
"""

SECOND_NF_CODE = """
### THIS SHOULD BE IMPORTED SEPARATELY ###
def check_2nf(s, primary_key, non_prime_attributes):
    # Check that each non-prime attribute depends on the entire primary key
    for non_prime in non_prime_attributes:
        for prime in primary_key:
            dependency_exists = has_fd(s, prime, non_prime)
            if not dependency_exists:
                return False
    return True

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
### Determinine 3NF

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
def check_3nf(s, non_prime_attributes):
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
                       nbf.v4.new_markdown_cell(DEPENDENCIES),
                       nbf.v4.new_code_cell(DEPENDENCIES_CODE),
                       nbf.v4.new_markdown_cell(CHECK_FOR_DEPENDENCY),
                       nbf.v4.new_code_cell(CHECK_FOR_DEPENDENCY_CODE),
                       nbf.v4.new_markdown_cell(SECOND_NF),
                       nbf.v4.new_code_cell(SECOND_NF_CODE),
                       nbf.v4.new_markdown_cell(THIRD_NF),
                       nbf.v4.new_code_cell(THIRD_NF_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "normalization-3nf/NORMALIZATION-3NF-CORE.ipynb" )
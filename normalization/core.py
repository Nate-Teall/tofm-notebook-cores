import nbformat as nbf

### Functional Dependencies ###

INTRO = """
## Database Normalization in Z3

In order to determine whether or not a relation is normalized, we must first know the functional dependencies.
Below is an example relation with 4 attributes:

$$ R_1(\\underline{studentID}, \\underline{courseID}, studentName, courseFee) $$

The relation has the following functional dependencies:

$$ studentID \\rightarrow studentName $$
$$ courseID \\rightarrow courseFee $$

It is clear that this relation is not normalized, because studentName and courseFee have partial dependcies on the primary key. We will use Z3 to prove this"""

RELATIONS = """
### Encoding Functional Dependencies

For two attributes X and Y, we say that X determines Y, $ X \\rightarrow Y $, if for any two rows in the relation:

$$ row1.X = row2.X \\rightarrow row1.Y = row2.Y $$

In other words, if two entities have the same value for attribute X, then they must have the same value in Y. 

In order to represent functional dependencies in Z3, we first need to create variables to represent two rows in the relation.
In the code below, we have created one variable for each attribute, for two arbitrary entities 'row1' and 'row2'.

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
Next, we will write a function to represent a functional dependency in the relation.
We will do this using the definition of a functional dependency.

**Complete the code below** to create a function that encodes a functional dependendency in Z3.
"""

DEPENDENCIES_CODE = """
def functional_dependency(X, Y):
    return Implies( False ) # REPLACE THIS LINE    

# Initialize solver
s = Solver()

# Add two functional dependencies
s.add( functional_dependency('studentID', 'studentName') )
s.add( functional_dependency('courseID', 'courseFee') )

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
s.add( functional_dependency('studentID', 'studentName') )

# Check if the FD exists:
print("studentID -> studentName :", has_fd(s, 'studentID', 'studentName'))
s.add( functional_dependency('courseID', 'courseFee') )

# Check for a non-existent FD:
print("studentID -> courseFee :", has_fd(s, 'studentID', 'courseFee'))
"""

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_markdown_cell(RELATIONS),
                       nbf.v4.new_code_cell(RELATIONS_CODE),
                       nbf.v4.new_markdown_cell(DEPENDENCIES),
                       nbf.v4.new_code_cell(DEPENDENCIES_CODE),
                       nbf.v4.new_markdown_cell(CHECK_FOR_DEPENDENCY),
                       nbf.v4.new_code_cell(CHECK_FOR_DEPENDENCY_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "normalization/NORMALIZATION-CORE.ipynb" )
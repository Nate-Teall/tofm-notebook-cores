import nbformat as nbf

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

# This cell was taken from the ASYMPTOTIC-BOUNDS notebook.
# It is not included within the IntegerConstraints core, but thought it would fit well to introduce the concept
SYSTEM_OF_EQUATIONS_TEXT = '''
Let's try an example with multiple equations. Replace lines in the code below to find a solution to the following system of equations:

$$x + 4y = 20$$
$$2x + 3y = 10$$
'''

SYSTEM_OF_EQUATIONS_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables

x = Real('x')
y = Real('y')

s.add( x + 4*y == 20 ) # add the first equation
s.add( False ) # REPLACE THIS LINE

showSolver( s ) # view the equations
'''

CHECK = '''print( s.check() ) # check if solution exists'''
MODEL = '''print( s.model() ) # output solution'''

REACTION1_TEXT = '''
## Reaction Balancing using Z3

Now that we know how to solve systems of equations using Z3, lets use this to balance the following reaction:

$$H_2 + O_2 \\rightarrow H_2O$$

To balance the reaction, we need to find coefficients x<sub>i</sub> for each compound that balances all elements.

$$x_1 \\cdot H_2 + x_2 \\cdot O_2 \\rightarrow x_3 \\cdot H_2O$$

Because O<sub>2</sub> contains twice as many oxygen atoms as H<sub>2</sub>O, the coefficient for H<sub>2</sub>O must be twice as big as the coefficient for O<sub>2</sub>.
So, to balance oxygen we can use the equation:

$$2 \\cdot x_2 = x_3$$

Similarly, we can use this equation to balance hydrogen:

$$2 \\cdot x_1 = 2 \\cdot x_3$$

Let's use Z3 to find the coefficients.
'''

# It might be more clear if we name the coefficients after the compound they are connected to,
# instead of x1, x2, etc...
REACTION1_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables
x1 = Int('x1') # Coefficient of H2
x2 = Int('x2') # Coefficient of O2
x3 = Int('x3') # Coefficient of H2O

# Add the equation to balance oxygen
s.add( 2*x2 == x3 ) 

# Add the equation to balance hydrogen
s.add( False ) # REPLACE THIS LINE

# Ensure each coefficient is positive!
s.add( x1 >= 1 )
s.add( x2 >= 1 )
s.add( x3 >= 1 )

showSolver( s ) # View the equations
print( s.check() ) # Check if solution exists
'''

REACTION1_OUTRO = '''
Great! You have successfully balanced the reaction:

$$2H_2 + O_2 \\rightarrow 2H_2O$$
'''

REACTION2_TEXT = '''
## Combustion of Propanol

Next, let's balance a more complex reaction, the combustion of propanol:

$$C_3H_7OH + O_2 \\rightarrow CO_2 + H_2O$$

To balance this reaction, we will need 4 coefficients, one for each compound:

$$x_1 \\cdot C_3H_7OH + x_2 \\cdot O_2 \\rightarrow x_3 \\cdot CO_2 + x_4 \\cdot H_2O$$

Because this reaction conatins 3 elements (C, H, and O), we will need three equations. One to balance each of them.
Replace the corresponding lines in the cell below to balance the reaction 
'''

REACTION2_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables
x1 = Int('x1') # Coefficient of Propanol
x2 = Int('x2') # Coefficient of O2
x3 = Int('x3') # Coefficient of CO2
x4 = Int('x4') # Coefficient of H2O

# REPLACE THE LINES BELOW
s.add( False ) # Balance carbon
s.add( False ) # Balance hydrogen
s.add( False ) # Balance oxygen


# Ensure each coefficient is positive!
s.add( x1 >= 1 )
s.add( x2 >= 1 )
s.add( x3 >= 1 )
s.add( x4 >= 1 )

showSolver( s ) # View the equations
print( s.check() ) # check if solution exists
'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(SYSTEM_OF_EQUATIONS_TEXT),
                       nbf.v4.new_code_cell(SYSTEM_OF_EQUATIONS_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(REACTION1_TEXT),
                       nbf.v4.new_code_cell(REACTION1_CODE),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(REACTION1_OUTRO),
                       nbf.v4.new_markdown_cell(REACTION2_TEXT),
                       nbf.v4.new_code_cell(REACTION2_CODE),
                       nbf.v4.new_code_cell(MODEL)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "REACTION-CORE.ipynb" )

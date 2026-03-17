import nbformat as nbf

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

# This cell was taken from the ASYMPTOTIC-BOUNDS notebook.
# It is not included within the IntegerConstraints core, but thought it would fit well to introduce the concept
SYSTEM_OF_EQUATIONS_TEXT = '''
Let's try an example with multiple equations. **Replace lines in the code below** to find a solution to the following system of equations:

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

To balance the reaction, we need to find coefficients for each compound that balances all elements.

To balance oxygen, the number of atoms of oxygen must be the same on both sides of the reaction. So, we will use this equation to model the amount on each side.
Here, $ C_X $ represents of the coefficient of that molecule.

$$2 \\cdot C_{H_2} = C_{H_2O}$$

Similarly, we can use this equation to balance hydrogen:

$$2 \\cdot C_{H_2} = 2 \\cdot C_{H_2O}$$

**Replace the line in the code below** to use Z3 to find the coefficients. 
'''

# It might be more clear if we name the coefficients after the compound they are connected to,
# instead of x1, x2, etc...
REACTION1_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables
H2 = Int('C_{H2}')   # Coefficient of H2
O2 = Int('C_{O2}')   # Coefficient of O2
H2O = Int('C_{H2O}') # Coefficient of H2O

# Add the equation to balance oxygen
s.add( 2*O2 == H2O ) 

# Add the equation to balance hydrogen
s.add( False ) # REPLACE THIS LINE

# Ensure each coefficient is positive!
s.add( H2 >= 1 )
s.add( O2 >= 1 )
s.add( H2O >= 1 )

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

To balance this reaction, we will need 4 coefficients, one for each compound. 
Because this reaction conatins 3 elements (C, H, and O), we will need three equations. One to balance each of them.

**Replace the corresponding lines in the cell below** to balance the reaction.
'''

REACTION2_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables
C3H7OH = Int('C_{C3H7OH}') # Coefficient of Propanol
O2 = Int('C_{O2}')         # Coefficient of O2
CO2 = Int('C_{O2}')        # Coefficient of CO2
H2O = Int('C_{H2O}')       # Coefficient of H2O

# REPLACE THE THREE LINES BELOW
s.add( False ) # Balance carbon
s.add( False ) # Balance hydrogen
s.add( False ) # Balance oxygen

# Ensure each coefficient is positive!
s.add( C3H7OH >= 1 )
s.add( O2 >= 1 )
s.add( CO2 >= 1 )
s.add( H2O >= 1 )

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
nbf.write( mynotebook, "reaction-balancing/REACTION-CORE.ipynb" )

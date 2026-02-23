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

AAAAAAAAAAAA = '''
# Initialize Z3 solver
s = Solver()

# Store into a data structure:
reactants = ["H2", "O2"]
products = ["H2O"]
compounds = {
    "H2": {"H": 2},
    "O2": {"O": 2},
    "H2O": {"H": 2, "O": 1}
}

def count_elements(equation_half, compounds):
  coefficients = []
  element_totals = {}

  for compound in equation_half:
    # Create a variable for the coefficient
    coefficient = Int(compound)
    coefficients.append(coefficient)

    # Create an equation to balance all of the 
    current_compound = compounds[compound]

    for element in current_compound:
      total = coefficient * current_compound[element]

      if element not in element_totals:
        element_totals[element] = total
      else:
        element_totals[element] += total
  
  return coefficients, element_totals

reactants_coef, reactants_eq = count_elements(reactants, compounds)
products_coef, products_eq = count_elements(products, compounds)

print(reactants_coef)
print(reactants_eq)

print(products_coef)
print(products_eq)

for element in reactants_eq:
  s.add(reactants_eq[element] == products_eq[element])

for coefficient in reactants_coef:
  s.add(coefficient >= 1)

for coefficient in products_coef:
  s.add(coefficient >= 1)

# Initialize variables
# x1 = Int('x1') # Coefficient of H2
# x2 = Int('x2') # Coefficient of O2
# x3 = Int('x3') # Coefficient of H2O

# Add the equation to balance oxygen
# s.add( 2*x2 == x3 )

# Add the equation to balance hydrogen
# s.add( 2*x1 == 2*x3 ) # REPLACE THIS LINE

# Ensure each coefficient is positive!
# s.add( x1 >= 1 )
# s.add( x2 >= 1 )
# s.add( x3 >= 1 )

showSolver( s ) # View the equations
print( s.check() ) # Check if solution exists
'''

INTRO_TEXT = '''
## Reaction Balancing using Z3

Recall that in the previous notebook, we wrote a program that balances the following reaction:

$$H_2 + O_2 \\rightarrow  H_2O$$

Let's see how we can improve on this to make a program that can balance more reactions. 
'''

STORING_EQ_TEXT = '''
### Representing Chemical Reaction

To write this program, we need a way to represent our reaction in python. 
To do this, we will use a dictionary to store each half of the reaction. 

In our example reaction, we have two reactants and one product, which we can represent as shown below.
Note that for each compound, we also need to know how much of each element is in it.
'''

STORING_EQ_CODE = '''
reactants = {
  'H2': {'H': 2},
  'O2': {'O': 2}
}

products = {
  'H2O': {'H': 2, 'O': 1}
}
'''

COUNT_ELEMENTS_TEXT = '''
### Calculating Element Totals

Recall that in the previous notebook, we found that balancing a reaction requires one variable for each coefficient, 
and one equation for each element.

To start, let's write a function that will create the variables
and an equation to represent the total amount of each element in one half of the reaction.

For our example reaction:

$$H_2 + O_2 \\rightarrow  H_2O$$

We need a coefficient for $ H_2 $ and $ O_2 $, as well as an equation to represent the number of hydrogen and oxygen atoms on the reactants side.
**Replace lines in the code below** to finish this function.
'''

COUNT_ELEMENTS_CODE = '''
def count_elements(reaction_half):
  # Create a list of coefficients
  coefficients = []
  # Create a dictionary that maps an element to an equation to calculate it's total on this half
  element_totals = {}
  
  for compound in equation_half:
  
    # Create a z3 variable for each coefficient
    coefficient = False # REPLACE THIS LINE
    coefficients.append( coefficient ) 

    # Count the amount of each element in this compound
    for element in compound:
      amount_of_element = compound[element]

      total = False # REPLACE THIS LINE

      if element not in element_totals:
        element_totals[element] = total
      else:
        element_totals[element] += total
  
  return coefficients, element_totals
'''

COUNT_ELEMENTS_TEST = '''
Test your function below by confirming that it correctly creates a variable for each compound on the reactants side of the equation:
'''

COUNT_ELEMENTS_TEST_CODE = '''
coefficients, element_totals = count_elements(reactants)

print( 'Coefficients for each reactant:', coefficients )
print( 'Total of each element:', element_totals )
'''

REACTION2_TEXT = '''
## Combustion of Propanol

Next, let's balance a more complex reaction, the combustion of propanol:

$$C_3H_7OH + O_2 \\rightarrow CO_2 + H_2O$$

To balance this reaction, we will need 4 coefficients, one for each compound. 
Because this reaction conatins 3 elements (C, H, and O), we will need three equations. One to balance each of them.
**Replace the corresponding lines in the cell below** to balance the reaction.
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

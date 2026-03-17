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

INTRO_TEXT = '''
## Reaction Balancing using Z3

Recall that in the previous notebook, we wrote a program that balances the following reaction:

$$H_2 + O_2 \\rightarrow  H_2O$$

Let's see how we can improve on this to make a program that can balance more reactions. 
'''

STORING_EQ_TEXT = '''
### Representing Chemical Reactions

To write this program, we need a way to represent our reaction in python. 
To do this, we will use a dictionary to store each half of the reaction. 

In our example reaction, we have two reactants and one product, which we can represent as shown below.
Note that for each compound, we create another dictionary that states how much of each element is in it.

No code is needed for this cell, **simply run the cell to create the variables**.
'''

STORING_EQ_CODE = '''
reactants = {
  'H2': {'H': 2},
  'O2': {'O': 2}
}

products = {
  'H2O': {'H': 2, 'O': 1} # 'Each molecule of H2O contains 2 hydrogen and 1 oxygen'
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

The equation should be the coefficient of the molecule times the amount of that element in that molecule.

**Replace lines in the code below** to finish this function.
'''

COUNT_ELEMENTS_CODE = '''
def count_elements(reaction_half):
  # Create a list of coefficients
  coefficients = []
  # Create a dictionary that maps an element to an equation that calculates the number of atoms of that element
  element_totals = {}
  
  for molecule in reaction_half:
  
    # Create a z3 variable for each coefficient
    coefficient = False # REPLACE THIS LINE

    coefficients.append( coefficient ) 

    elements = reaction_half[molecule]
    for element in elements:
    
      # Create an equation that calculates the amount atoms of this element in the molecule
      amount_of_element = elements[element]
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

BALANCE_REACTION_TEXT = '''
### Balancing Both Sides

Great! All that is left is to use this function to balance both halves of the reaction. 
Remember, in order to balance the reaction, we must ensure the amount of an element on both sides is *equal*. 

**Replace lines in the code below** to finish the full function
'''

BALANCE_REACTION_CODE = '''
def create_reaction_solver(reactants, products):
  s = Solver()

  # Get the coefficients and equations for both sides
  reactants_coef, reactants_totals = count_elements(reactants)
  products_coef, products_totals = count_elements(products)

  # Ensure the amount of each element is the same on reactants and products side
  for element in reactants_totals:
    s.add( False ) # REPLACE THIS LINE

  coefficients = reactants_coef + products_coef
  
  # Ensure all coefficients are positive
  for coefficient in coefficients:
    s.add( False ) # REPLACE THIS LINE

  return s
'''

BALANCE_REACTION_TEST = '''
Let's test our function with the example reaction!
'''

BALANCE_REACTION_TEST_CODE = '''
reactants = {
  'H2': {'H': 2},
  'O2': {'O': 2}
}

products = {
  'H2O': {'H': 2, 'O': 1}
}

s = create_reaction_solver(reactants, products)

showSolver( s ) # View the equations
print( s.check() ) # Check if solution exists
'''

REACTION2_TEXT = '''
### Combustion of Propanol

Great! Let's test our function one last time with a more complex reaction, the combustion of propanol.

$$C_3H_7OH + O_2 \\rightarrow CO_2 + H_2O$$

**Replace the lines in the code below** to input the above reaction into our solver.
'''

REACTION2_CODE = '''
reactants = { } # REPLACE THIS LINE

products = { } # REPLACE THIS LINE

s = create_reaction_solver(reactants, products)

showSolver( s ) # View the equations
print( s.check() ) # Check if solution exists
'''


### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(SYSTEM_OF_EQUATIONS_TEXT),
                       nbf.v4.new_code_cell(SYSTEM_OF_EQUATIONS_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),

                       nbf.v4.new_markdown_cell(INTRO_TEXT),
                       nbf.v4.new_markdown_cell(STORING_EQ_TEXT),
                       nbf.v4.new_code_cell(STORING_EQ_CODE),

                       nbf.v4.new_markdown_cell(COUNT_ELEMENTS_TEXT),
                       nbf.v4.new_code_cell(COUNT_ELEMENTS_CODE),
                       nbf.v4.new_markdown_cell(COUNT_ELEMENTS_TEST),
                       nbf.v4.new_code_cell(COUNT_ELEMENTS_TEST_CODE),

                       nbf.v4.new_markdown_cell(BALANCE_REACTION_TEXT),
                       nbf.v4.new_code_cell(BALANCE_REACTION_CODE),
                       nbf.v4.new_markdown_cell(BALANCE_REACTION_TEST),
                       nbf.v4.new_code_cell(BALANCE_REACTION_TEST_CODE),
                       nbf.v4.new_code_cell(MODEL),

                       nbf.v4.new_markdown_cell(REACTION2_TEXT),
                       nbf.v4.new_code_cell(REACTION2_CODE),
                       nbf.v4.new_code_cell(MODEL)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "reaction-balancing-advanced/REACTION-ADVANCED-CORE.ipynb" )

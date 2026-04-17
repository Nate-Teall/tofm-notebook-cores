import nbformat as nbf

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

INTRO = '''## Determining Limiting Reactants using Z3

For the rest of this notebook, we will walk through solving a limiting reactants problem with Z3.

The reaction we will study is the combustion of propane. The balanced reaction is:

$$ C_3H_8 + 5O_2 \\rightarrow 3CO_2 + 4H_2O $$

We will determine the limiting reactant when given 2 moles of propane and 5 moles of oxygen.

To model the problem, we must create variables to represent three things: The starting amount of each reactant in moles, the amount of each reactant used, and the amount of products produced.
'''

VARIABLES = '''# Initialize Solver
s = Solver()

# 1) Variables to represent the initial amount of propane and oxygen
initial_C3H8 = 2
initial_O2 = 8

# 2) Variables to represent the amount of propane and oxygen consumed
consumed_C3H8 = Real('Consumed_{C_3H_8}')
consumed_O2 = Real('Consumed_{O_2}')

# 3) Variables to represent the final amount of CO2 and H2O
produced_CO2 = Real('Produced_{CO_2}')
produced_H2O = Real('Produced_{H_2O}')'''

EXTENT = '''Lastly, we will use a variable to represent the "extent" of the reaction. 
This represents how much of the reaction can be completed with the given amounts.

For example, in our reaction, if we were given one mole of $C_3H_8$ and five moles $O_2$, the full reaction can completed once, so the extent is one.
If we were given half as much of each, the extent would be one half.'''

EXTENT_CODE = '''extent = Real('X')'''

CONSTRAINTS = '''Great! Now we need to add constraints to the solver.

First, we must determine the amount of reactants used, and products created, based on the extent of the reaction.

**Replace the lines below** to implement these constraints.'''

CONSTRAINTS_CODE = '''# The amount of each reactant used depends on the extent of the reaction. We multiply the extent by the stoichiometric coefficient to find this.
s.add(consumed_C3H8 == extent * 1)
s.add(consumed_O2 == 0) # REPLACE THIS LINE

# We use a similar process to determine how much of each product was created, based on the extent of the reaction.
s.add(extent * 3 == produced_CO2)
s.add(0 == produced_H2O) # REPLACE THIS LINE'''

LIMITING_LOGIC = '''Finally, the last thing to do is add the limiting reactant logic.
The amount of reactants used cannot be more than what we are initially given.

**Replace the line below** to implement this in Z3.'''

LIMITING_CODE = '''# Limiting Reactant Logic
s.add(consumed_C3H8 <= 0) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE

# Let's view our solver so far
showSolver(s)'''

OPTIMIZER = '''Great! We have completed our model of the problem. The last thing to do is determine how far the reaction can go.

In our case, we need to do more than just find values of the variables that satisfy the equations.
We want to know how far the reaction is able to go until we run out of either reactant. 
In other words, we want to know what the *maximum* value for the extent is.

To do this, we will use Z3's Optimizer. This class is very similar to solver, as it also requires a set of variables and constraints. 
However, instead of finding any correct value for each variable, it allows us to find the maximum or minimum values of certain variables.

Run the cell below to create the Optimizer.'''

OPTIMIZER_CODE = '''# Initialize the Optimizer
opt = Optimize()

# Copy the variables and constraints from our solver
opt.add(s.assertions())

# Tell the optimizer to maximize the extent of the reaction
opt.maximize(extent)'''

CHECK_OPT = '''print( opt.check() ) # check if solution exists'''

MODEL = '''To better visualize the results, we have created a function to print the model.

You should see that the limiting reactant was O2, as all 8 mols were consumed.'''

MODEL_CODE = '''
m = opt.model()

# THIS SHOULD BE IMPORTED
extent = float(m[extent].as_decimal(5))
print(f"Reaction Extent: {extent}")
print(f"CO2 Produced: {m[produced_CO2].as_decimal(2)} mol")
print(f"H2O Produced: {m[produced_H2O].as_decimal(2)} mol")
print(f"Consumed C3H8: {m[consumed_C3H8].as_decimal(2)} mol")
print(f"Consumed O2: {m[consumed_O2].as_decimal(2)} mol\\n")

print(f"Remaining C3H8: {initial_C3H8 - float(m[consumed_C3H8].as_decimal(2))} mol")
print(f"Remaining O2: {initial_O2 - float(m[consumed_O2].as_decimal(2))} mol")
'''



### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_code_cell(VARIABLES),
                       nbf.v4.new_markdown_cell(EXTENT),
                       nbf.v4.new_code_cell(EXTENT_CODE),
                       nbf.v4.new_markdown_cell(CONSTRAINTS),
                       nbf.v4.new_code_cell(CONSTRAINTS_CODE),
                       nbf.v4.new_markdown_cell(LIMITING_LOGIC),
                       nbf.v4.new_code_cell(LIMITING_CODE),
                       nbf.v4.new_markdown_cell(OPTIMIZER),
                       nbf.v4.new_code_cell(OPTIMIZER_CODE),
                       nbf.v4.new_code_cell(CHECK_OPT),
                       nbf.v4.new_markdown_cell(MODEL),
                       nbf.v4.new_code_cell(MODEL_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "limiting-reactant/LIMITING-REACTANT-CORE.ipynb" )

import nbformat as nbf

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

INTRO = '''## Drawing Lewis Structures using Z3

Now that we have familiarized ourselves with Z3, lets see how we can use it to draw the Lewis Structure of a molecule.
The molecule we will start with is $ CO_2 $. 

To draw the Lewis Structure, we must first determine the number of valence electrons. Carbon as 4, and each oxygen has 6, giving a total of 16.
Now, we have to determine how these electrons will be distributed as bond pairs or lone pairs.

In this molecule, carbon is the central atom, so the bonds will be between the carbon atom and the two oxygen. 
We can represent the number of bond and lone pairs for each atom as variables.
'''

VARIABLES = '''# Initialize Solver
s = Solver()

# Set the total number of valence electrons
total_valence = 16

# Number Lone Pairs
C = Int('C')
O2 = Int('O^2')
O1 = Int('O^1')

# Number of Bond Pairs
C_O1 = Int('C-O^1')
C_O2 = Int('C-O^2')'''

CONSTRAINTS = '''Great! Our next step is to add the constraints.

Recall that to create the lewis structure, all valence electrons must be distributed. 
So, the total number of pairs time two should equal our total number of electrons 

Second, the octet rule states each atom must have a full shell of 8 valence electrons. 
In other words, each element must have 4 electron pairs in total.

Lastly, we know that carbon and oxygen must be bonded, so there is at least a single bond between those atoms.

**Replace the lines below** to encode the constrains using Z3.'''

CONSTRAINTS_CODE = '''# 1) The number of electrons distributed must equal 16
s.add((O1 + 1) * 2 == total_valence) # REPLACE THIS LINE

# 2) The octet rule: Each atom must have 4 pairs in total, whether bond or lone pairs.
s.add(O1 + C_O1 == 4)   # All pairs of the first oxygen atom
s.add(O2 == 4)          # REPLACE THIS LINE
s.add(False)            # REPLACE THIS LINE

# 3) Each bond must be at least a single bond
s.add(C_O1 >= 1)
s.add(False) # REPLACE THIS LINE

# Let's view the solver 
showSolver(s)'''

OPTIMIZER = '''Finally, there is one last constraint we need to add. 

Remember, some molecules have multiple valid structures, or resonance structures.
The most significant resonance structure has a minimum formal charge.
If possible, the number of lone pairs for the outer oxygen atoms should be equal.

We can accomplish this using the Z3 Optimizer, as shown below.'''

OPTIMIZER_CODE = '''opt = Optimize()
opt.add(s.assertions())

# If the number of lone pairs are equal, then the value will be 0. 
opt.minimize(abs(O2 - O1))'''

SOLUTION = '''Now that we've created the solver, all that's left is to view the solution!'''

CHECK = '''print( opt.check() ) # check if solution exists'''

MODEL = '''print( opt.model() ) # output solution'''

VIEW = '''To better view the solution, we've defined a function to draw the structure'''

VIEW_CODE = '''#draw_lewis(opt)'''



### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_code_cell(VARIABLES),
                       nbf.v4.new_markdown_cell(CONSTRAINTS),
                       nbf.v4.new_code_cell(CONSTRAINTS_CODE),
                       nbf.v4.new_markdown_cell(OPTIMIZER),
                       nbf.v4.new_code_cell(OPTIMIZER_CODE),
                       nbf.v4.new_markdown_cell(SOLUTION),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(VIEW),
                       nbf.v4.new_code_cell(VIEW_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "lewis-structures/LEWIS-STRUCUTRES-CORE.ipynb" )

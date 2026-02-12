import nbformat as nbf
import base64

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

# Get image data
# This function was written by the Google AI
with open("master-theorem/plot.png", "rb") as f:
    image_bytes = f.read()
    encoded_plot = base64.b64encode(image_bytes).decode('utf-8')

image_uri = f"data:image/png;base64,{encoded_plot}"

# The first few tutorial cells were taken from the ASYMPTOTIC-BOUNDS notebook.
# It is not included within the IntegerConstraints core, but thought it would fit well to introduce the concept
SYSTEM_OF_EQUATIONS_TEXT = '''
Now it's your turn! Now it's your turn! **Replace lines in the code below** to find a solution to the following system of equations:

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

COMPARE_F_G_TEXT = f'''
Let's look at a slightly more complicated example of what we can achieve with Z3. Consider the following two functions which have also been plotted below:
$$f(x) = 4x$$
$$g(x) = x^2$$

<center>

![Plot of F and G]({image_uri})

</center>

Note that when $x \geq 4$, we have $g(x) \geq f(x)$. Let's see how we can prove this using Z3.

Formally, we have to show the following:
$$\\forall x : x \geq 4 \implies x^2 \geq 4x$$

i.e., for every real $x$, $x \geq 4$ implies that $x^2 \geq 4x$. Let's see how we can encode this using Z3.
'''
COMPARE_F_G_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables

x = Real('x')

# Initialize Functions

f = 4*x
g = pow( x, 2 ) # pow(x,y) is equivalent to x^y

# Construct constraint

impliesConstraint = Implies( x >= 4, g >= f )
# Implies( a, b ) is equivalent to "a ==> b"

forAllConstraint = ForAll( x, impliesConstraint )
# ForAll( a, b ) is equivalent to "For All a : b"

s.add( forAllConstraint  ) # add the constraint

showSolver( s ) # view the constraint
'''

COMPARE_F_G_TEXT2 = '''
Recall that "sat" means that Z3 has verified the statement for us, so we have succesfully proven that $\\forall x : x \geq 4 \implies x^2 \geq 4x$ !
**Now try it yourself! Complete the code below to show that for all values of $x$ in the range $[0,4]$, we have $4x \geq x^2$.**
'''

COMPARE_F_G_CODE2 = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables

x = Real('x')

# Initialize Functions

f = 4*x
g = pow( x, 2 )

# Construct constraint

xRangeConstraint = And( x >= 0, x <= 4 )
# And(a,b) is equivalent to "a and b"

impliesConstraint = Implies( xRangeConstraint, False ) # REPLACE THIS LINE

forAllConstraint = ForAll( x, False ) # REPLACE THIS LINE

s.add( forAllConstraint  ) # add the constraint

showSolver( s ) # view the constraint
s.check()
'''

### Master Theorem ###

MASTER_THEOREM_INTRO = '''
## Applying the Master Theorem in Z3

Recall that the Master Theorem can be used to determine the time complexity, T(n), of divide an conquer algorithms:

$$ T(n) = a T(\\frac{n}{b}) + f(n) $$

Here, f(n) is the time complexity of splitting the problem into smaller parts and combining the solutions.
The Master Theorem lets us determine the overall complexity of the function, by analyzing the complexity of f(n).

1. If $ f(n) = O(n^{log_ba-\epsilon}) $, then $ T(n) = \Theta(log_ba) $ 
2. If 


'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(SYSTEM_OF_EQUATIONS_TEXT),
                       nbf.v4.new_code_cell(SYSTEM_OF_EQUATIONS_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(COMPARE_F_G_TEXT),
                       nbf.v4.new_code_cell(COMPARE_F_G_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_markdown_cell(MASTER_THEOREM_INTRO)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "master-theorem/MASTER-THEOREM-CORE.ipynb" )
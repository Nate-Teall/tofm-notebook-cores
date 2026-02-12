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
'''



### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(SYSTEM_OF_EQUATIONS_TEXT),
                       nbf.v4.new_code_cell(SYSTEM_OF_EQUATIONS_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(COMPARE_F_G_TEXT)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "MASTER-THEOREM-CORE.ipynb" )
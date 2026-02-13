import nbformat as nbf
import base64

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
from math import log
'''

# Get image data
# This function was written by the Google AI
with open("master-theorem/plot.png", "rb") as f:
    image_bytes = f.read()
    encoded_plot = base64.b64encode(image_bytes).decode('utf-8')

image_uri = f"data:image/png;base64,{encoded_plot}"

# The first few tutorial cells were taken from the ASYMPTOTIC-BOUNDS notebook.
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

CHECK = '''print( s.check() ) # check if true'''

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

# I'm not sure if it would be nicer to have the example be a more familiar algorithm, like merge sort, 
# but that is a pretty trivial case
MASTER_THEOREM_INTRO = '''
## Applying the Master Theorem in Z3

Recall that the Master Theorem can be used to determine the time complexity, T(n), of divide an conquer algorithms:

$$ T(n) = a T(\\frac{n}{b}) + f(n) $$

Here, f(n) is the time complexity of combining the solutions of each smaller part.
The Master Theorem lets us determine the overall complexity of the function, by comparing the complexity of f(n) to the number of recursive calls the algorithm makes.

1. If $ f(n) = O(n^{log_ba-\epsilon}) $, then $ T(n) = \Theta(n^{log_ba}) $ 
2. If $ f(n) = \Theta(n^{log_ba}) $, then $ T(n) = \Theta(n^{log_ba} \cdot logn) $ 
3. If $ f(n) = \Omega(n^{log_ba-\epsilon}) $, then $ T(n) = \Theta(f(n)) $

Where $\epsilon$ is some constant > 0

Now, we will use Z3 to determine the time complexity of some algorithm. The recurrence relation we will be using is:

$$ T(n) = 8T(\\frac{n}{4}) + n^{1.5} $$
'''

CASE_1_TEXT = '''
### Checking Case 1

Recall that for two functions $f(n)$ and $g(n)$ we say that $f(n)=O(g(n))$ if and only if there exist constants $c$ and $n_0$ such that

$$\\forall n : n \\geq n_0 \\implies c \\cdot g(n) \\geq f(n)$$

Using Z3's capabilities that we explored above, we have made the following function to check whether $f(n)=O(g(n))$ given two functions $f$ and $g$ in terms of $n$.
'''

BIG_O_CODE = '''
def makeBigOSolver( f, g ):
  n, c, n0 = Reals('n c n_0')

  # Constraints
  c_positive = c > 0
  big_o_condition = ForAll( n , Implies( n >= n0 , c*g >= f ) )

  s = Solver()
  s.add( c_positive )
  s.add( big_o_condition )
  return s

def bigO( f, g ):
  s = makeBigOSolver( f, g )
  return s.check() == sat
'''

CASE_2_TEXT = '''
### Checking Case 2 and 3

Now that we have written a function to test case 1, we will now write one to check case 2 and 3. 

Recall that $ f = \Theta(g) $ if BOTH $ f = O(g) $ and $ f = \Omega(g) $ are true. 

For two functions $f(n)$ and $g(n)$ we say that $f(n)=\\Omega(g(n))$ if and only if there exist constants $c$ and $n_0$ such that

$$\\forall n : n \\geq n_0 \\implies f(n) \\geq c \\cdot g(n)$$
**Complete the code below to make a function that shows $f(n)=\\Omega(g(n))$ as in the function above:**
'''

OMEGA_CODE = '''
def makeBigOmegaSolver( f, g ):
  n, c, n0 = Reals('n c n_0')

  # Constraints
  c_positive = c > 0
  big_omega_condition = ForAll( n , False ) # REPLACE THIS LINE

  s = Solver()
  s.add( c_positive )
  s.add( big_omega_condition )
  return s

def bigOmega( f, g ):
  s = makeBigOmegaSolver( f, g )
  return s.check() == sat
'''

MASTER_THEOREM_TEXT = '''
### Putting it All Together

Finally, we can write a function to determine which case of the master theorem applies to our algorithm.

Remember, the recurrence relation is:

$$ T(n) = 8T(\\frac{n}{4}) + n^{1.5} $$

**Complete the code below** by filling in the correct values for a, b and f(n).
'''

MASTER_THEOREM_CODE = '''
def masterTheoremSolver( n, a, b, f ):
  g = pow( n, log(a, b) )

  isBigO = bigO( f, g )
  isBigOmega = bigOmega( f, g )
  isTheta = isBigO and isBigOmega

  if isTheta:
    print("f = Theta(g), Case 2!")
  elif isBigO:
    print("f = O(g), Case 1!") 
  elif isBigOmega:
    print("f = Omega(g), Case 3!") 

n = Real( 'n' )
a = False     # REPLACE THIS LINE
b = False     # REPLACE THIS LINE
f = pow(0, 0) # REPLACE THIS LINE
masterTheoremSolver( n, a, b, f )
'''

OUTRO = '''
Now we have determined that $ f(n) = \Theta(n^{log_ba}) $. 

Since case 2 applies, you have now proven that $ T(n) = \Theta(n^{1.5} \cdot logn) $ ! 
'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(COMPARE_F_G_TEXT),
                       nbf.v4.new_code_cell(COMPARE_F_G_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_markdown_cell(COMPARE_F_G_TEXT2),
                       nbf.v4.new_code_cell(COMPARE_F_G_CODE2),
                       nbf.v4.new_markdown_cell(MASTER_THEOREM_INTRO),
                       nbf.v4.new_markdown_cell(CASE_1_TEXT),
                       nbf.v4.new_code_cell(BIG_O_CODE),
                       nbf.v4.new_markdown_cell(CASE_2_TEXT),
                       nbf.v4.new_code_cell(OMEGA_CODE),
                       nbf.v4.new_markdown_cell(MASTER_THEOREM_TEXT),
                       nbf.v4.new_code_cell(MASTER_THEOREM_CODE),
                       nbf.v4.new_markdown_cell(OUTRO)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "master-theorem/MASTER-THEOREM-CORE.ipynb" )
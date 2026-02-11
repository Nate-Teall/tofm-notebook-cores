import nbformat as nbf
import requests

# This cell was taken from the ASYMPTOTIC-BOUNDS notebook.
# It is not included within the IntegerConstraints core, but thought it would fit well
SYSTEM_OF_EQUATIONS_TEXT = '''
"unsat" means the system is not satisfiable, i.e., there is no real number 
that satisfies all the constraints we gave to the solver. Note that if we were to run s.model() now we would get an error.

Now it's your turn! Replace lines in the code below to find a solution to the following system of equations:

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

$$x<sub>1</sub> * H<sub>2</sub> + x<sub>2</sub> * O<sub>2</sub> &rarr x<sub>1</sub> * H<sub>2</sub>O$$

To balance the reaction, we need to find the values for each coefficient x that balances each element.


Because O<sub>2</sub> contains twice as many oxygen atoms as H<sub>2</sub>O, the coefficient for H<sub>2</sub>O must be twice as big as the coefficient for O<sub>2</sub>.
So, to balance oxygen we can use the equation:

$$2 * x<sub>2</sub> = x<sub>3</sub>

Similarly, we can use this equation to balance hydrogen:

$$2 * x<sub>1</sub = 2 * x<sub>3</sub>

Let's use Z3 to find the coefficients.
'''

# It might be more clear if we name the coefficients after the compound they are connected to,
# instead of x1, x2, etc...
REACTION1_CODE = '''
# Initialize Z3 solver
s = Solver()

# Initialize variables
x1 = Int('x1')
x2 = Int('x2')
x3 = Int('x3')

s.add( 2*x2 == x3 ) # Add the equation to balance oxygen
s.add( 2*x1 == 2*x3 ) # Add the equation to balance hydrogen

showSolver( s ) # View the equations
'''

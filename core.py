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

SYSTEM_OF_EQUATIONS_CHECK = '''print( s.check() ) # check if solution exists'''
SYSTEM_OF_EQUATIONS_MODEL = '''print( s.model() ) # output solution'''

REACTION1_TEXT = '''
## Reaction Balancing using Z3

Now that we know how to solve systems of equations using Z3, lets use this to balance the following reaction:

$$x<sub>1</sub> * H<sub>2</sub> + x<sub>2</sub> * O<sub>2</sub> &rarr x<sub>1</sub> * H<sub>2</sub>O$$

To balance the reaction, we need to find the values for each coefficient x that balances each element.


Because O<sub>2</sub> contains twice as many oxygen atoms as H<sub>2</sub>O, the coefficient for H<sub>2</sub>O must be twice as big as the coefficient for O<sub>2</sub>.
So, to balance oxygen we can use the equation:

$$x<sub>2</sub> * 2 = x<sub>3</sub>

Similarly, we can use this equation to balance hydrogen:

$$x<sub>1</sub> * 2 = x<sub>3</sub> * 2

Let's use Z3 to find the coefficients.
'''

REACTION1_CODE = '''

'''
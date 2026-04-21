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
O1 = Int('O^1')
O2 = Int('O^2')

# Number of Bond Pairs
C_O1 = Int('CO^1')
C_O2 = Int('CO^2')'''

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

CHECK_OPT = '''print( opt.check() ) # check if solution exists'''

MODEL_OPT = '''print( opt.model() ) # output solution'''

VIEW = '''To better view the solution, we've defined a function to draw the structure. 

NOTE: Bond angles are not accurate. This is only meant to display the electron placement.'''

VIEW_CODE_OPT = '''m = opt.model()
draw_lewis_from_model(m)'''

VIEW_FUNCS = '''# Should be imported
def draw_lewis_from_model(m):
  """Converts a model to the format required by draw_lewis_structure"""
  # List of elements
  elements = []
  # List of bond variables
  bonds = []
  lone_pairs = []

  # Add element names and lone pairs to the list
  for d in m.decls():
    name = d.name()
    if len(name) == 1 or name[1] == '^':
      elements.append(name)
      lone_pairs.append(m[d].as_long())

  # Add bond pair counts
  for d in m.decls():
    name = d.name()
    # Bond Pairs
    if len(name) > 1 and name[1] != '^':
      bonds.append((elements.index(name[0]), elements.index(name[1:4]), m[d].as_long()))
  
  draw_lewis_structure(elements, bonds, lone_pairs)


# WRITTEN BY GEMINI
def draw_lewis_structure(elements, bonds, lone_pairs):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    ax.axis('off')

    # 1. Coordinate Setup (Circle Layout)
    n = len(elements)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = {i: np.array([np.cos(a), np.sin(a)]) / 3 for i, a in enumerate(angles)}

    # 2. Draw Bonds with Multi-bond Offsets
    for idx1, idx2, count in bonds:
        p1, p2 = pos[idx1], pos[idx2]
        vec = p2 - p1
        perp = np.array([-vec[1], vec[0]])
        perp = perp / np.linalg.norm(perp) * 0.05

        # Offset multi-bonds slightly so they don't overlap
        offsets = np.linspace(-0.6, 0.6, count) if count > 1 else [0]
        for opt in offsets:
            shift = perp * opt
            ax.plot([p1[0] + shift[0], p2[0] + shift[0]], 
                    [p1[1] + shift[1], p2[1] + shift[1]], 
                    color='black', lw=2, zorder=1)

    # 3. Draw Atoms and Distributed Lone Pairs
    for i, (el, lp_count) in enumerate(zip(elements, lone_pairs)):
        x, y = pos[i]
        ax.text(x, y, el[0], fontsize=28, fontweight='bold', ha='center', va='center', 
                bbox=dict(facecolor='white', edgecolor='none', pad=1.5), zorder=2)

        # Calculate angles to neighbors to find "open" slots
        neighbor_angles = []
        for b1, b2, _ in bonds:
            if b1 == i: neighbor_angles.append(np.arctan2(pos[b2][1]-y, pos[b2][0]-x))
            if b2 == i: neighbor_angles.append(np.arctan2(pos[b1][1]-y, pos[b1][0]-x))

        # Standard slots: 0, 90, 180, 270 degrees
        potential_slots = [0, np.pi/2, np.pi, 3*np.pi/2]
        available_slots = []
        
        for slot in potential_slots:
            # Only use slot if it's not pointing toward a bond
            if not any(abs((slot - na + np.pi) % (2*np.pi) - np.pi) < 0.5 for na in neighbor_angles):
                available_slots.append(slot)

        # Draw lone pairs in the best available slots
        for lp_idx in range(min(lp_count, len(available_slots))):
            slot_angle = available_slots[lp_idx]
            dist = 0.1
            # The two dots of the pair are slightly separated perpendicular to the slot angle
            dot_gap = 0.03
            for side in [-1, 1]:
                dx = x + dist * np.cos(slot_angle) + side * dot_gap * np.sin(slot_angle)
                dy = y + dist * np.sin(slot_angle) - side * dot_gap * np.cos(slot_angle)
                ax.scatter(dx, dy, s=40, color='red', zorder=3) # Red for visibility

    plt.show()'''

NI3 = '''## Lewis Structure of Nitrogen Triiodide

Great work! Next, lets try a slightly larger molecule, $ NI_3 $.

In this molecule, nitrogen is the central atom, bonded to three iodine.

**Replace lines in the code below** to create the solver for this molecule.'''

NI3_CODE = '''# Initialize Solver
s = Solver()

# Set the total number of valence electrons
total_valence = 0 # REPLACE THIS LINE

# Number Lone Pairs
N = Int('N')
I1 = Int('I^1')
I2 = Int('I^2')
I3 = Int('I^3')

# Number of Bond Pairs
N_I1 = Int('NI^1')
N_I2 = Int('NI^2')
N_I3 = Int('NI^3')

# 1) The number of electrons distributed must equal 16
s.add((I1) * 2 == total_valence) # REPLACE THIS LINE

# 2) The octet rule: Each atom must have 4 pairs in total, whether bond or lone pairs.
s.add(False) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE

# 3) Each bond must be at least a single bond
s.add(False) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE
s.add(False) # REPLACE THIS LINE

# Let's view the solver 
showSolver(s)'''

CHECK = '''print( s.check() ) # check if solution exists'''
MODEL = '''print( s.model() ) # output solution'''

VIEW_2 = '''When you think your solution is correct, use the cell below to visualize it.'''

VIEW_CODE = '''m = opt.model()
draw_lewis_from_model(m)'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_code_cell(VARIABLES),
                       nbf.v4.new_markdown_cell(CONSTRAINTS),
                       nbf.v4.new_code_cell(CONSTRAINTS_CODE),
                       nbf.v4.new_markdown_cell(OPTIMIZER),
                       nbf.v4.new_code_cell(OPTIMIZER_CODE),
                       nbf.v4.new_markdown_cell(SOLUTION),
                       nbf.v4.new_code_cell(CHECK_OPT),
                       nbf.v4.new_code_cell(MODEL_OPT),
                       nbf.v4.new_markdown_cell(VIEW),
                       nbf.v4.new_code_cell(VIEW_FUNCS),
                       nbf.v4.new_code_cell(VIEW_CODE_OPT),
                       nbf.v4.new_markdown_cell(NI3),
                       nbf.v4.new_code_cell(NI3_CODE),
                       nbf.v4.new_code_cell(CHECK),
                       nbf.v4.new_code_cell(MODEL),
                       nbf.v4.new_markdown_cell(VIEW_2),
                       nbf.v4.new_code_cell(VIEW_CODE)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "lewis-structures/LEWIS-STRUCUTRES-CORE.ipynb" )

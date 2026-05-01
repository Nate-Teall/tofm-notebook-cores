import nbformat as nbf

IMPORTS = '''!pip install z3-solver
!pip install git+https://github.com/crrivero/FormalMethodsTasting.git#subdirectory=core
from z3 import *
from tofmcore import showSolver
'''

EXTRA_IMPORTS = '''### SHOULD BE IMPORTED ###
def draw_all_matchings(s, all_sols, num_center):
  # Draw in a grid with 3 columns
  rows = len(all_sols) // 3
  fig, axs = plt.subplots(rows,3, figsize=(12,12))
  axes = axs.flatten()

  for i, sol in enumerate(all_sols):
    draw_single_matching(sol, axes[i], num_center)

def draw_single_matching(m, ax, num_center):
  # Create the edges and the matchings from the solution
  edges = []
  matching = []
  for i in m:
    val = m[i]
    a = str(i)[3]
    b = str(i)[4]
    edges.append((a, b))
    if val:
      matching.append((a, b))

  # Create the graph from the edges.
  G = nx.Graph()
  G.add_edges_from(sorted(edges)) # Sorting ensures consisten layout of nodes
  edge_colors = ['red' if e in matching or (e[1], e[0]) in matching else 'black' for e in G.edges()]

  # Draw graph aligned to grid
  draw_chemical_graph(G, edge_colors, [str(i+1) for i in range(num_center)], ax)

### Written by Gemini ###
def draw_chemical_graph(G, edge_colors, centerline_nodes, ax):
    """
    centerline_nodes: a list of nodes to be placed on the y=0 axis.
    """
    pos = {}

    # 1. Position the centerline nodes
    for i, node in enumerate(centerline_nodes):
        pos[node] = (i, 0)

    # 2. Position the children above/below
    for parent in centerline_nodes:
        # Find neighbors not already in the centerline
        children = [n for n in G.neighbors(parent) if n not in centerline_nodes]

        for i, child in enumerate(children):
            # Alternate: even index above (1), odd index below (-1)
            x_offset = pos[parent][0]
            y_offset = 1 if i % 2 == 0 else -1
            pos[child] = (x_offset, y_offset)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=700,
            node_color='white', edge_color=edge_colors, ax=ax)'''

INTRO = '''## Matching using Z3

In this notebook, we will look at an application of the matching problem in chemistry. 
We will see how the Z-index chemical graph corresponds to the boiling point of the molecule.

The molecule we will be looking at are three different isomers of Hexane, $ C_6H_{14} $:

IMAGE HERE
'''

CHEMICAL_GRAPH = '''### The Z Index

The Z Index of a molecule is the number of matchings within its chemical graph. 
A chemical graph is structure where the nodes represent atoms, and edges represent the bonds. Hydrogen atoms are excluded.

Below is the chemical graph of the first isomer we will be looking at:

IMAGE HERE

A matching is a selection of the edges such each node has at most one of their edges selected. We will use Z3 to find all possible matchings for this isomer. 
'''

STEP_1 = '''#### Step 1: Make boolean values for each edge#### Step 1: Make boolean variables for each edge

In our solution, an edge with the value of True will represent an edge that has been selected in our matching.'''

STEP_1_CODE = '''# In the graph above, carbon 1 shares an edge with carbon 2, so we will represent that with the variable e_12
e12 = Bool('e_{12}')

# We follow the same conventiion for all other edges in the graph
e23 = Bool('e_{23}')
e34 = Bool('e_{34}')
e25 = Bool('e_{25}')
e26 = Bool('e_{26}')

vars = [e12, e23, e34, e25, e26]'''

STEP_2 = '''#### Step 2: Initialize Solver'''

STEP_2_CODE = '''s = Solver()'''

STEP_3 = '''#### Step 3: Write Constraints'''

STEP_3_CODE = '''# Carbon atom 2 can have at most one edge adjacent to it in the matching
s.add(e12 + e23 + e25 + e26 <= 1)

# Carbon atom 3 can have at most one edge adjacent to it in the matching
s.add(e23 + e34 <= 1)

# The rest of the atoms have only one edge, so no constraints are necessary!

# Let's see what the constraints look like
showSolver(s)
'''

STEP_4 = '''#### Step 4: Check if a solution exists'''

STEP_4_CODE = '''print( s.check() )'''

VIEW_SOLS = '''Great! Now we can determine how many matchings there are, and visualize them. We have defined a function to find and show all matchings'''

VIEW_SOLS_CODE = '''all_solutions = list_all_solutions(s, vars)
print( 'Number of matchings:', len(all_solutions) )
draw_all_matchings(s, all_solutions, 4)'''

PROBLEM_2 = '''Great! We have successfully determined the Z Index of this molecule.

Now its your turn! **Complete the code below** to determine the Z Index of the next isomer:

IMAGE HERE'''

PROBLEM_2_CODE = '''# Initialize Solver
s = Solver()

# In the graph above, carbon 1 shares an edge with carbon 2, so we will represent that with the variable e_12
e12 = Bool('e_{12}')

# We follow the same conventiion for all other edges in the graph
e23 = Bool('e_{23}')
e34 = Bool('e_{34}')
e45 = Bool('e_{45}')
e26 = Bool('e_{26}')
vars = [e12, e23, e34, e45, e26]

# Carbon atom 2 can have at most one edge adjacent to it in the matching
s.add(False)

# Carbon atom 3 can have at most one edge adjacent to it in the matching
s.add(False)

# Do the same for Carbon 4
s.add(False)

# The rest of the atoms have only one edge

# Let's see what the constraints look like
showSolver(s)
'''

VIEW_SOLS_2_CODE = '''all_solutions = list_all_solutions(s, vars)
print( 'Number of matchings:', len(all_solutions) )
draw_all_matchings(s, all_solutions, 5)'''

PROBLEM_3 = '''Lastly, let's determine the Z Index of one more isomer, and compare it to their boiling points

**Complete the code below** to determine the Z Index of the final isomer:

IMAGE HERE'''

PROBLEM_3_CODE = '''# Initialize Solver
s = Solver()

# In the graph above, carbon 1 shares an edge with carbon 2, so we will represent that with the variable e_12
e12 = Bool('e_{12}')

# We follow the same conventiion for all other edges in the graph
e23 = Bool('e_{23}')
e34 = Bool('e_{34}')
e45 = Bool('e_{45}')
e56 = Bool('e_{56}')
vars = [e12, e23, e34, e45, e56]

# Carbon atom 2 can have at most one edge adjacent to it in the matching
s.add(False)

# Carbon atom 3 can have at most one edge adjacent to it in the matching
s.add(False)

# Do the same for Carbon 4
s.add(False)

# Do the same for Carbon 5
s.add(False)

# The rest of the atoms have only one edge

# Let's see what the constraints look like
showSolver(s)'''

VIEW_SOLS_3_CODE = '''all_solutions = list_all_solutions(s, vars)
print( 'Number of matchings:', len(all_solutions) )
draw_all_matchings(s, all_solutions, 6)'''

CONCLUSION = '''Great! Now we can compare the results to show that the Z-Index correlates to boiling point.
| Isomer | Z Index | Boiling Point |
| ------ | ------- | ------------- |
| 1      | 9       | 49.7          |
| 2      | 11      | 60.2          |
| 3      | 13      | 68.7          |'''

### Build the notebook ###
mynotebook = nbf.v4.new_notebook()

mynotebook['cells'] = [nbf.v4.new_code_cell(EXTRA_IMPORTS),
                       nbf.v4.new_markdown_cell(INTRO),
                       nbf.v4.new_markdown_cell(CHEMICAL_GRAPH),
                       nbf.v4.new_markdown_cell(STEP_1),
                       nbf.v4.new_code_cell(STEP_1_CODE),
                       nbf.v4.new_markdown_cell(STEP_2),
                       nbf.v4.new_code_cell(STEP_2_CODE),
                       nbf.v4.new_markdown_cell(STEP_3),
                       nbf.v4.new_code_cell(STEP_3_CODE),
                       nbf.v4.new_markdown_cell(STEP_4),
                       nbf.v4.new_code_cell(STEP_4_CODE),
                       nbf.v4.new_markdown_cell(VIEW_SOLS),
                       nbf.v4.new_code_cell(VIEW_SOLS_CODE),
                       nbf.v4.new_markdown_cell(PROBLEM_2),
                       nbf.v4.new_code_cell(PROBLEM_2_CODE),
                       nbf.v4.new_code_cell(STEP_4_CODE),
                       nbf.v4.new_code_cell(VIEW_SOLS_2_CODE),
                       nbf.v4.new_markdown_cell(PROBLEM_3),
                       nbf.v4.new_code_cell(PROBLEM_3_CODE),
                       nbf.v4.new_code_cell(STEP_4_CODE),
                       nbf.v4.new_code_cell(VIEW_SOLS_3_CODE),
                       nbf.v4.new_markdown_cell(CONCLUSION)]

nbf.validator.normalize( mynotebook )
nbf.validate( mynotebook )
nbf.write( mynotebook, "matching/Z-INDEX.ipynb" )

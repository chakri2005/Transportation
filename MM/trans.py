import random
from scipy.optimize import linear_sum_assignment
from IPython.display import display, HTML, Box

def generate_random_costs(F, S, min_cost=1, max_cost=10):
    """
    Generates a random transportation cost matrix.

    Args:
        F: Number of factories.
        S: Number of stores.
        min_cost: Minimum cost per unit (inclusive).
        max_cost: Maximum cost per unit (inclusive).

    Returns:
        A 2D array containing random transportation costs.
    """
    c = [[random.randint(min_cost, max_cost) for _ in range(S)] for _ in range(F)]
    return c

# Get user input for number of factories and stores
F = int(input("Enter the number of factories: "))
S = int(input("Enter the number of stores: "))

# Initialize a list to store transportation costs entered by the user
user_costs = []

# Prompt user for random cost generation or manual input
choice = input("Generate random transportation costs (y/n)? ")

if choice.lower() == 'y':
    # Generate random costs
    c = generate_random_costs(F, S)
    print("Random Transportation Costs:")
    for row in c:
        print(row)
    user_costs = c
else:
    # Get user input for transportation costs
    c = []
    for i in range(F):
        row = []
        for j in range(S):
            cost = int(input(f"Enter transportation cost for Factory {i+1} to Store {j+1}: "))
            row.append(cost)
        c.append(row)
    user_costs = c

# Display the entered values in a box form
box = Box(children=[HTML("<h3>User Entered Values</h3>"), HTML("<pre>{}</pre>".format('\n'.join(['\t'.join(map(str, row)) for row in user_costs])))])
display(box)

# ... (define remaining data entities: p, a, d)

# Solve the transportation problem
cost, x = linear_sum_assignment(user_costs, maximize=False)

# Print the optimal transportation plan and total cost
total_cost = sum(cost[i][j] * x[i][j] for i in range(F) for j in range(S))
print("Optimal Transportation Plan:")
for i in range(F):
    for j in range(S):
        print(f"Factory {i+1} to Store {j+1}: {x[i][j]} units")
print("Total Transportation Cost:", total_cost)

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

# Prompt user for random cost generation or manual input
choice = input("Generate random transportation costs (y/n)? ")

if choice.lower() == 'y':
  # Generate random costs
  c = generate_random_costs(F, S)
  print("Random Transportation Costs:")
  for row in c:
    print(row)
else:
  # Get user input for transportation costs
  c = []
  for i in range(F):
    row = []
    for j in range(S):
      cost = int(input(f"Enter transportation cost for Factory {i+1} to Store {j+1}: "))
      row.append(cost)
    c.append(row)

# Get user input for factory availabilities and store requirements
factory_availability = [0 for _ in range(F)]  # Initialize with zeros
store_requirement = [0 for _ in range(S)]  # Initialize with zeros

# Get user input for factory availabilities
print("Enter production capacity (availability) for each factory:")
for i in range(F):
  availability = int(input(f"Factory {i+1}: "))
  factory_availability[i] = availability

# Get user input for store requirements (demand)
print("Enter demand (requirement) for each store:")
for j in range(S):
  requirement = int(input(f"Store {j+1}: "))
  store_requirement[j] = requirement

# Basic feasibility check (total supply vs. total demand)
total_supply = sum(factory_availability)
total_demand = sum(store_requirement)
if total_supply != total_demand:
  print("Error: Total supply does not meet total demand. The problem might not have a feasible solution.")
  exit()  # Exit the program if supply and demand don't match

# ... (Optional: Modify cost calculation or introduce constraints based on availability and requirement)

# Solve the transportation problem (adapt based on your chosen library)
cost, x = linear_sum_assignment(c, maximize=False)

# Print the optimal transportation plan and total cost
total_cost = sum(cost[i][j] * x[i][j] for i in range(F) for j in range(S))
print("Optimal Transportation Plan:")
for i in range(F):
  for j in range(S):
    print(f"Factory {i+1} to Store {j+1}: {x[i][j]} units")
print("Total Transportation Cost:", total_cost)

#include <iostream>
#include <limits> // for numeric_limits
#include <glpk.h>

using namespace std;

void generate_random_costs(int F, int S, int min_cost, int max_cost, int c[][S]) {
  // Use Mersenne Twister engine for better randomness
  random_device rd;
  mt19937 gen(rd());
  uniform_int_distribution<int> dis(min_cost, max_cost);

  for (int i = 0; i < F; i++) {
    for (int j = 0; j < S; j++) {
      c[i][j] = dis(gen);
    }
  }
}

int main() {
  int F, S;

  cout << "Enter the number of factories: ";
  cin >> F;
  cout << "Enter the number of stores: ";
  cin >> S;

  char choice;
  cout << "Generate random transportation costs (y/n)? ";
  cin >> choice;

  int c[F][S];

  if (choice == 'y' || choice == 'Y') {
    int min_cost, max_cost;
    cout << "Enter minimum cost per unit: ";
    cin >> min_cost;
    cout << "Enter maximum cost per unit: ";
    cin >> max_cost;

    // Validate user input for cost range
    if (min_cost < 0 || min_cost > max_cost) {
      cerr << "Error: Minimum cost must be non-negative and less than or equal to maximum cost." << endl;
      return 1; // Exit with error code
    }

    generate_random_costs(F, S, min_cost, max_cost, c);
    cout << "\nRandom Transportation Costs:\n";
    for (int i = 0; i < F; i++) {
      for (int j = 0; j < S; j++) {
        cout << c[i][j] << " ";
      }
      cout << endl;
    }
  } else {
    // Get user input for transportation costs
    for (int i = 0; i < F; i++) {
      for (int j = 0; j < S; j++) {
        cout << "Enter transportation cost for Factory " << i + 1 << " to Store " << j + 1 << ": ";
        cin >> c[i][j];
      }
    }
  }

  // Define data entities (assuming you have production cost (p), production capacity (a), and demand (d) arrays)

  // **Solve the transportation problem using GLPK**

  // Initialize GLPK environment
  glp_prob lp = glp_create_prob();
  glp_set_prob_name(lp, "Transportation Problem");

  // Define objective function (minimize total transportation cost)
  glp_set_obj_dir(lp, GLP_MIN);

  // Add variables (x[i][j]) representing units shipped from factory i to store j
  int num_vars = F * S;
  for (int i = 0; i < F; i++) {
    for (int j = 0; j < S; j++) {
      int var_id = glp_add_var(lp, 1);
      glp_set_var_name(lp, var_id, ("X_" + to_string(i + 1) + "_" + to_string(j + 1)).c_str());
      glp_set_var_type(lp, var_id, GLP_INT); // Set variables as integer (optional for transportation problems)
      glp_set_obj_coef(lp, var_id, c[i][j]); // Set objective function coefficients (transportation costs)
    }
  }

  // Add supply constraints (total shipped from each factory <= production capacity)
  for (int i = 0; i < F; i++) {
    int constraint_id = glp_add_row(lp);
    glp_set_row_name(lp, constraint_id, ("Supply_" + to_string(i + 1)).c_str());
    for (int j = 0; j < S; j++) {
      int var_id = (i * S) +

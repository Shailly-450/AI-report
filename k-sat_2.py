import random
import time

def generate_3sat_problem(num_clauses, num_variables):
    """Generate num_clauses of 3-SAT with num_variables."""
    clauses = []
    for _ in range(num_clauses):
        clause = random.sample(range(1, num_variables + 1), 3)  # Select 3 distinct variables
        clause = [random.choice([var, -var]) for var in clause]  # Negate each variable with 50% probability
        clauses.append(clause)
    return clauses

def count_satisfied_clauses(clauses, assignment):
    """Count how many clauses are satisfied by the given assignment."""
    satisfied = 0
    for clause in clauses:
        if any((var > 0 and assignment[var - 1]) or (var < 0 and not assignment[-var - 1]) for var in clause):
            satisfied += 1
    return satisfied

def run_hill_climbing(clauses, num_variables):
    """Hill Climbing algorithm for solving 3-SAT."""
    current_assignment = [random.choice([True, False]) for _ in range(num_variables)]
    current_satisfied = count_satisfied_clauses(clauses, current_assignment)

    for _ in range(1000):  # Limit the number of iterations
        next_assignment = current_assignment[:]
        var_to_flip = random.randint(0, num_variables - 1)  # Select a random variable to flip
        next_assignment[var_to_flip] = not next_assignment[var_to_flip]

        next_satisfied = count_satisfied_clauses(clauses, next_assignment)
        if next_satisfied > current_satisfied:
            current_assignment = next_assignment
            current_satisfied = next_satisfied

    return current_assignment, current_satisfied

def run_beam_search(clauses, num_variables, beam_width):
    """Beam Search algorithm for solving 3-SAT."""
    beam = [[random.choice([True, False]) for _ in range(num_variables)]]
    
    for _ in range(100):  # Limit the number of iterations
        next_beam = []
        for assignment in beam:
            for var in range(num_variables):
                next_assignment = assignment[:]
                next_assignment[var] = not next_assignment[var]
                next_beam.append(next_assignment)

        # Select the best assignments based on satisfaction count
        next_beam.sort(key=lambda x: count_satisfied_clauses(clauses, x), reverse=True)
        beam = next_beam[:beam_width]  # Keep the best beam_width assignments

    # Return the best solution from the final beam
    best_assignment = max(beam, key=lambda x: count_satisfied_clauses(clauses, x))
    best_satisfied = count_satisfied_clauses(clauses, best_assignment)
    return best_assignment, best_satisfied

def run_variable_neighborhood_descent(clauses, num_variables):
    """Variable Neighborhood Descent algorithm for solving 3-SAT."""
    current_assignment = [random.choice([True, False]) for _ in range(num_variables)]
    current_satisfied = count_satisfied_clauses(clauses, current_assignment)
    
    for _ in range(1000):  # Limit the number of iterations
        improvement_found = False
        for var in range(num_variables):
            next_assignment = current_assignment[:]
            next_assignment[var] = not next_assignment[var]  # Flip variable
            
            next_satisfied = count_satisfied_clauses(clauses, next_assignment)
            if next_satisfied > current_satisfied:
                current_assignment = next_assignment
                current_satisfied = next_satisfied
                improvement_found = True
                break
        
        if not improvement_found:
            break  # No improvements found, exit the loop

    return current_assignment, current_satisfied

def main():
    # Take user input for m, n, and trials
    num_clauses = int(input("Enter the number of clauses (m): "))
    num_variables = int(input("Enter the number of variables (n): "))
    num_trials = int(input("Enter the number of trials: "))

    for trial in range(num_trials):
        print(f"\nTrial {trial + 1}:")
        
        # Generate a random 3-SAT problem
        clauses = generate_3sat_problem(num_clauses, num_variables)

        # Run Hill Climbing
        print("Running Hill Climbing...")
        start_time = time.time()
        hc_solution, hc_satisfied = run_hill_climbing(clauses, num_variables)
        hc_time = time.time() - start_time
        print(f"Hill Climbing: {hc_satisfied}/{num_clauses} clauses satisfied with {hc_solution} in {hc_time:.4f} seconds")

        # Run Beam Search with width 3
        print("\nRunning Beam Search with beam width 3...")
        start_time = time.time()
        bs_solution, bs_satisfied = run_beam_search(clauses, num_variables, beam_width=3)
        bs_time = time.time() - start_time
        print(f"Beam Search (width 3): {bs_satisfied}/{num_clauses} clauses satisfied with {bs_solution} in {bs_time:.4f} seconds")

        # Run Beam Search with width 4
        print("\nRunning Beam Search with beam width 4...")
        start_time = time.time()
        bs_solution, bs_satisfied = run_beam_search(clauses, num_variables, beam_width=4)
        bs_time = time.time() - start_time
        print(f"Beam Search (width 4): {bs_satisfied}/{num_clauses} clauses satisfied with {bs_solution} in {bs_time:.4f} seconds")

        # Run Variable Neighborhood Descent
        print("\nRunning Variable Neighborhood Descent...")
        start_time = time.time()
        vnd_solution, vnd_satisfied = run_variable_neighborhood_descent(clauses, num_variables)
        vnd_time = time.time() - start_time
        print(f"Variable Neighborhood Descent: {vnd_satisfied}/{num_clauses} clauses satisfied with {vnd_solution} in {vnd_time:.4f} seconds")

# Run the main function
if __name__ == "_main_":
    main()
import random

def generate_k_sat(k, m, n):
    if k > n:
        raise ValueError("k must be less than or equal to n (number of variables).")

    clauses = []

    for _ in range(m):
        # Generate k distinct variable indices
        variables = random.sample(range(1, n + 1), k)
        # Randomly decide to negate each variable
        clause = [(var if random.choice([True, False]) else -var) for var in variables]
        clauses.append(clause)

    return clauses

def main():
    try:
        # User input for k, m, and n
        k = int(input("Enter the number of variables in each clause (k): "))
        m = int(input("Enter the number of clauses (m): "))
        n = int(input("Enter the number of variables (n): "))

        # Generate and print k-SAT problem
        k_sat_problem = generate_k_sat(k, m, n)
        print("\nGenerated k-SAT Problem:")
        for i, clause in enumerate(k_sat_problem, 1):
            print(f"Clause {i}: {clause}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "_main_":
    main()
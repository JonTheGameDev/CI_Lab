from itertools import product

def get_num_variables():
    """Get the number of variables from the user."""
    while True:
        try:
            num_vars = int(input("How many variables do you want to use? "))
            if num_vars <= 0:
                print("Please enter a positive number.")
                continue
            return num_vars
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_variable_names(num_vars):
    """Get variable names from the user."""
    variables = []
    for i in range(num_vars):
        name = input(f"Enter name for variable {i+1}: ").strip()
        if not name:
            name = f"Var{i+1}"
        variables.append(name)
    return variables

def generate_combinations(variables):
    """Generate all possible combinations of True/False for the variables."""
    return list(product([True, False], repeat=len(variables)))

def get_user_distribution(variables):
    """Get probabilities for all combinations from the user."""
    combinations = generate_combinations(variables)
    default_prob = 1.0 / len(combinations)  # Uniform distribution as default
    
    print(f"\nEnter probabilities for each combination (or press Enter for default {default_prob:.4f}).")
    print(f"Sum of all probabilities must equal 1.0\n")
    
    joint_distribution = {}
    for combo in combinations:
        prompt = f"P({', '.join(f'{var}={val}' for var, val in zip(variables, combo))}): "
        val = input(prompt)
        if val.strip() == '':
            prob = default_prob
        else:
            try:
                prob = float(val)
            except ValueError:
                print("Invalid input, using default value.")
                prob = default_prob
        joint_distribution[combo] = prob
    
    total = sum(joint_distribution.values())
    if abs(total - 1.0) > 1e-6:
        print(f"\nWarning: Probabilities sum to {total}, not 1.0. Normalizing.")
        for key in joint_distribution:
            joint_distribution[key] /= total
    
    return joint_distribution

def print_joint_distribution(joint_distribution, variables):
    """Print the joint probability distribution in a formatted table."""
    print("\nFull Joint Probability Distribution:")
    header = '\t'.join(variables) + '\tProbability'
    print(header)
    print("-" * len(header))
    for combo, prob in joint_distribution.items():
        row = '\t'.join(str(val) for val in combo) + f'\t{prob:.6f}'
        print(row)

def get_inference_query(variables):
    """Get an inference query from the user."""
    print("\nEnter your inference query (comma-separated conditions).")
    print(f"Example: {variables[0]}=True,{variables[1] if len(variables) > 1 else 'Var2'}=False")
    query = input("Query (leave blank for none): ")
    
    if not query.strip():
        return {}
    
    evidence = {}
    conditions = query.split(",")
    for cond in conditions:
        if '=' in cond:
            var, val = cond.split('=')
            var = var.strip()
            val = val.strip().lower() == 'true'
            evidence[var] = val
    
    return evidence

def infer(joint_distribution, variables, evidence):
    if not evidence:
        return None
    
    num = 0.0
    for combo, prob in joint_distribution.items():
        assign = {var: val for var, val in zip(variables, combo)}
        match_evidence = all(assign.get(var) == val for var, val in evidence.items())
        if match_evidence:
            num += prob
    
    return num

def main():
    print("\n")
    
    # Get number of variables
    num_vars = get_num_variables()
    
    # Get variable names
    variables = get_variable_names(num_vars)
    print(f"\nVariables: {', '.join(variables)}")
    
    # Get joint probability distribution
    joint_distribution = get_user_distribution(variables)
    
    # Print the distribution
    print_joint_distribution(joint_distribution, variables)
    
    # Inference loop
    while True:
        evidence = get_inference_query(variables)
        if evidence:
            prob = infer(joint_distribution, variables, evidence)
            print(f"\nP({', '.join(f'{var}={val}' for var, val in evidence.items())}) = {prob:.6f}")
        else:
            print("No inference query provided.")
        
        cont = input("\nPerform another query? (y/n): ").strip().lower()
        if cont != 'y':
            break
    
    print("exiting...")

if __name__ == "__main__":
    main()
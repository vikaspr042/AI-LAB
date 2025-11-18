import itertools

# ----- Step 1: Define propositional symbols -----
symbols = ['R', 'W']  # R: It rains, W: Ground is wet

# ----- Step 2: Define knowledge base (KB) -----
def KB(model):
    """Returns True if the KB is true in the given model."""
    R = model['R']
    W = model['W']
    # KB: (R → W) ∧ R
    return ((not R or W) and R)

# ----- Step 3: Define query -----
def QUERY(model):
    """Query: Is the ground wet (W)?"""
    return model['W']

# ----- Step 4: Truth table enumeration algorithm -----
def entails(KB, QUERY, symbols):
    print("Truth Table Evaluation:\n")
    print("R\tW\tKB\tQ\tModel Valid?")
    print("-"*40)
    all_models = list(itertools.product([True, False], repeat=len(symbols)))

    kb_true_models = []
    entailment_holds = True

    for values in all_models:
        model = dict(zip(symbols, values))
        kb_val = KB(model)
        q_val = QUERY(model)

        print(f"{model['R']}\t{model['W']}\t{kb_val}\t{q_val}", end='\t')

        if kb_val:
            kb_true_models.append(model)
            if not q_val:
                entailment_holds = False
                print("❌")
            else:
                print("✅")
        else:
            print("-")

    print("\nModels where KB is True:")
    for m in kb_true_models:
        print(m)

    return entailment_holds

# ----- Step 5: Run entailment check -----
result = entails(KB, QUERY, symbols)

print("\nRESULT:")
if result:
    print("✅ Query is ENTAILED by the Knowledge Base.")
else:
    print("❌ Query is NOT entailed by the Knowledge Base.")

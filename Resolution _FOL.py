
from collections import deque
import pandas as pd

# ---------- Utility Functions ----------
def neg(lit):
    """Return negation of literal"""
    return lit[1:] if lit.startswith('-') else '-' + lit

def clause_to_str(clause):
    """Readable string for a clause"""
    return " ∨ ".join(sorted(clause, key=lambda x: x.strip('-'))) if clause else "{} (empty clause)"

# ---------- Knowledge Base ----------
# Clauses from grounded example (Anil, peanuts)
clauses = [
    frozenset(['Alive_Anil']),                                    # C1
    frozenset(['-Alive_Anil', 'NotKilled_Anil']),                 # C2
    frozenset(['Eats_Anil_Peanuts']),                             # C3
    frozenset(['-Eats_Anil_Peanuts', '-NotKilled_Anil', 'Food_Peanuts']), # C4
    frozenset(['-Food_Peanuts', 'John_likes_peanuts']),           # C5
    frozenset(['-John_likes_peanuts'])                            # C6 (negated goal)
]

# ---------- Resolution Function ----------
def resolve(ci, cj):
    resolvents = set()
    for li in ci:
        comp = neg(li)
        if comp in cj:
            new_clause = set(ci.union(cj))
            new_clause.discard(li)
            new_clause.discard(comp)
            resolvents.add(frozenset(new_clause))
    return resolvents

# ---------- Resolution Process ----------
clauses_list = list(clauses)
clause_indices = {clauses_list[i]: i + 1 for i in range(len(clauses_list))}
derived_steps = []
step = 0

print("\n=== INITIAL CLAUSES ===")
for c in clauses_list:
    print(f"C{clause_indices[c]}: {clause_to_str(c)}")

print("\n=== STARTING RESOLUTION ===\n")
new_added = True
max_steps = 200

while new_added and step < max_steps:
    new_added = False
    current = list(clauses_list)
    for i in range(len(current)):
        for j in range(i + 1, len(current)):
            ci, cj = current[i], current[j]
            resolvents = resolve(ci, cj)
            for r in resolvents:
                step += 1
                # skip tautologies
                if any(neg(l) in r for l in r):
                    continue
                if r not in clause_indices:
                    clauses_list.append(r)
                    clause_indices[r] = len(clause_indices) + 1
                    resolved_lit = next((l for l in ci if neg(l) in cj), "?")
                    derived_steps.append((clause_indices[r], clause_indices[ci], clause_indices[cj], resolved_lit, clause_to_str(r)))
                    print(f"Step {step}: Resolve C{clause_indices[ci]} and C{clause_indices[cj]} on '{resolved_lit}'")
                    print(f"    Derived C{clause_indices[r]}: {clause_to_str(r)}\n")
                    new_added = True
                    # check for contradiction
                    if len(r) == 0:
                        print(">>> Empty clause {} derived. CONTRADICTION reached!")
                        print(">>> Therefore, the KB entails the query: John_likes_peanuts ✅\n")
                        # create proof table
                        df = pd.DataFrame(derived_steps, columns=["Derived", "From", "With", "ResolvedLiteral", "Clause"])
                        print("=== DERIVATION TABLE ===")
                        print(df.to_string(index=False))
                        exit()

print("Resolution finished without deriving the empty clause (no proof found).")


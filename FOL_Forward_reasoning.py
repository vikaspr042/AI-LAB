from copy import deepcopy
from itertools import product

# -------------------- Utility functions --------------------

def is_variable(x):
    """Check if a symbol is a variable (starts with lowercase)."""
    return isinstance(x, str) and len(x) > 0 and x[0].islower()

def substitute(atom, theta):
    """Substitute variable bindings in an atom."""
    pred, args = atom
    return (pred, tuple(theta.get(a, a) for a in args))

def unify_var(var, x, theta):
    """Unify variable with another term."""
    if var in theta:
        return unify(theta[var], x, theta)
    if is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    theta[var] = x
    return theta

def unify(a, b, theta=None):
    """Unify two terms or atoms and return the substitution."""
    if theta is None:
        theta = {}
    if isinstance(a, tuple) and isinstance(b, tuple):
        pa, aa = a[0], a[1]
        pb, ba = b[0], b[1]
        if pa != pb or len(aa) != len(ba):
            return None
        for va, vb in zip(aa, ba):
            theta = unify(va, vb, theta)
            if theta is None:
                return None
        return theta
    else:
        if a == b:
            return theta
        if is_variable(a):
            return unify_var(a, b, theta)
        if is_variable(b):
            return unify_var(b, a, theta)
        return None

# -------------------- Rule and Knowledge Base --------------------

class Rule:
    """Represents a Horn clause rule."""
    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents  # list of atoms
        self.consequent = consequent    # single atom
    def __repr__(self):
        ants = " ∧ ".join([f"{p}{a}" for p, a in self.antecedents])
        return f"{ants} => {self.consequent[0]}{self.consequent[1]}"

class FOLKB:
    """Forward chaining knowledge base."""
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.derived_steps = []

    def add_fact(self, atom, source="given"):
        if atom not in self.facts:
            self.facts.add(atom)
            self.derived_steps.append(f"Derived fact {atom} ({source})")
            return True
        return False

    def add_rule(self, rule):
        self.rules.append(rule)

    def forward_chain(self, query=None, max_iter=1000):
        """Perform forward chaining until no new facts or query proven."""
        new_added = True
        iter_count = 0
        while new_added and iter_count < max_iter:
            iter_count += 1
            new_added = False
            for rule in self.rules:
                # Rename variables in the rule to avoid clashes
                var_map = {}
                fresh_ants = []
                fresh_cons = deepcopy(rule.consequent)

                def freshen_term(t):
                    if is_variable(t):
                        if t not in var_map:
                            var_map[t] = f"{t}_{iter_count}"
                        return var_map[t]
                    return t

                for p, args in rule.antecedents:
                    fresh_ants.append((p, tuple(freshen_term(a) for a in args)))
                fresh_cons = (fresh_cons[0], tuple(freshen_term(a) for a in fresh_cons[1]))

                # Match antecedents with known facts
                candidate_facts_lists = []
                for (p, a) in fresh_ants:
                    candidate_facts_lists.append([f for f in self.facts if f[0] == p and len(f[1]) == len(a)])

                # Try all combinations of matching facts
                for combo in product(*candidate_facts_lists):
                    theta = {}
                    fail = False
                    for ant_atom, fact_atom in zip(fresh_ants, combo):
                        theta = unify(ant_atom, fact_atom, theta)
                        if theta is None:
                            fail = True
                            break
                    if fail:
                        continue

                    # Infer new fact
                    inferred = substitute(fresh_cons, theta)
                    if self.add_fact(inferred, source=f"from rule {rule} using {combo}"):
                        new_added = True
                        if query is not None and unify(inferred, query) is not None:
                            return True
        return (query is None) or (any(unify(f, query) is not None for f in self.facts))

# -------------------- Build Knowledge Base --------------------

file_citation = "Week-8-AI-lab-FOL-ForwardChaining.pdf"

kb = FOLKB()

# Existential instantiation: ∃x Owns(A,x) ∧ Missile(x)
kb.add_fact(("Owns", ("A", "t1")), source=f"existential-instantiation {file_citation}")
kb.add_fact(("Missile", ("t1",)), source=f"existential-instantiation {file_citation}")

# Given facts
kb.add_fact(("American", ("Robert",)), source=file_citation)
kb.add_fact(("Enemy", ("A", "America")), source=file_citation)

# Rules from the lab slides
kb.add_rule(Rule([("Missile", ("x",))], ("Weapon", ("x",))))
kb.add_rule(Rule([("Enemy", ("x", "America"))], ("Hostile", ("x",))))
kb.add_rule(Rule([("Missile", ("x",)), ("Owns", ("A", "x"))], ("Sells", ("Robert", "x", "A"))))
kb.add_rule(Rule([("American", ("p",)), ("Weapon", ("q",)), ("Sells", ("p", "q", "r")), ("Hostile", ("r",))], ("Criminal", ("p",))))

# Query
query = ("Criminal", ("Robert",))

# -------------------- Run Forward Chaining --------------------

print("Knowledge base forward chaining run based on:", file_citation)
print("\nInitial Facts:")
for f in sorted(kb.facts):
    print(" ", f)

print("\nRules:")
for r in kb.rules:
    print(" ", r)

print("\nRunning forward chaining... (showing derivation steps)\n")
result = kb.forward_chain(query=query)

for step in kb.derived_steps:
    print(step)

print("\nFinal Facts in KB:")
for f in sorted(kb.facts):
    print(" ", f)

print(f"\nQuery {query} proved? -> {result}")

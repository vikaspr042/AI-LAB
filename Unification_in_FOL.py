# ---------------------------------------------------------------
# Unification in First Order Logic (Robinson's Algorithm)
# ---------------------------------------------------------------

import re

# ---------- Helper functions ----------

def split_args(s):
    """Split comma-separated arguments considering nested parentheses."""
    args, cur, depth = [], '', 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            args.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args

def parse_term(s):
    """Parse a term like f(x,g(y)) or X."""
    s = s.strip()
    if '(' not in s:
        if s[0].islower():   # variable if starts lowercase
            return ('var', s)
        else:                # constant if uppercase
            return ('const', s)
    name, inside = s.split('(', 1)
    args = split_args(inside[:-1])
    return ('func', name.strip(), tuple(parse_term(a) for a in args))

def term_to_str(t):
    """Convert parsed term back to string."""
    if t[0] == 'var':
        return t[1]
    if t[0] == 'const':
        return t[1]
    return f"{t[1]}({', '.join(term_to_str(a) for a in t[2])})"

def apply_subs(term, subs):
    """Apply substitutions recursively."""
    if term[0] == 'var':
        if term[1] in subs:
            return apply_subs(subs[term[1]], subs)
        return term
    elif term[0] == 'func':
        return ('func', term[1], tuple(apply_subs(a, subs) for a in term[2]))
    return term

def occurs_check(var, term, subs):
    """Prevent infinite loops like x = f(x)."""
    term = apply_subs(term, subs)
    if term[0] == 'var':
        return term[1] == var
    elif term[0] == 'func':
        return any(occurs_check(var, a, subs) for a in term[2])
    return False

# ---------- Core Unification Algorithm ----------

def unify(t1, t2, subs=None, trace=None):
    if subs is None:
        subs = {}
    if trace is None:
        trace = []

    t1 = apply_subs(t1, subs)
    t2 = apply_subs(t2, subs)

    trace.append(f"Trying to unify {term_to_str(t1)} with {term_to_str(t2)}")

    # identical
    if t1 == t2:
        trace.append(" → Terms identical. No substitution needed.")
        return subs, trace

    # variable case
    if t1[0] == 'var':
        return unify_var(t1[1], t2, subs, trace)
    if t2[0] == 'var':
        return unify_var(t2[1], t1, subs, trace)

    # constant conflict
    if t1[0] == 'const' and t2[0] == 'const':
        trace.append(f" ✗ Conflict: constants {t1[1]} and {t2[1]} do not match.")
        return None, trace

    # function or predicate
    if t1[0] == 'func' and t2[0] == 'func':
        if t1[1] != t2[1] or len(t1[2]) != len(t2[2]):
            trace.append(" ✗ Function name or arity mismatch.")
            return None, trace
        for a1, a2 in zip(t1[2], t2[2]):
            subs, trace = unify(a1, a2, subs, trace)
            if subs is None:
                return None, trace
        return subs, trace

    trace.append(" ✗ Cannot unify terms.")
    return None, trace

def unify_var(var, term, subs, trace):
    if var in subs:
        trace.append(f" {var} already substituted by {term_to_str(subs[var])}. Continuing...")
        return unify(subs[var], term, subs, trace)
    if occurs_check(var, term, subs):
        trace.append(f" ✗ Occurs check failed: {var} appears in {term_to_str(term)}")
        return None, trace
    subs[var] = term
    trace.append(f" ✓ Substitute {var} → {term_to_str(term)}")
    return subs, trace

# ---------- Example Execution ----------

examples = [
    ("Eats(x, Apple)", "Eats(Riya, y)"),
    ("Knows(John, x)", "Knows(x, Elisabeth)"),
    ("likes(John, z)", "likes(x, f(y))"),
    ("f(x)", "f(g(x))")
]

for s1, s2 in examples:
    print("="*70)
    print(f"Unifying: {s1}  AND  {s2}\n")
    t1, t2 = parse_term(s1), parse_term(s2)
    subs, trace = unify(t1, t2)
    for step in trace:
        print("  " + step)
    if subs:
        result = {k: term_to_str(v) for k,v in subs.items()}
        print("\n✅ Final Substitutions:", result)
    else:
        print("\n❌ Unification failed.")
    print("="*70 + "\n")

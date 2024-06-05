class Fact:
    def __init__(self, predicate, args):
        self.predicate = predicate
        self.args = args
    
    def __repr__(self):
        return f"{self.predicate}({', '.join(self.args)})"

class Rule:
    def __init__(self, conclusion, antecedents):
        self.conclusion = conclusion
        self.antecedents = antecedents

    def __repr__(self):
        antecedents_str = ', '.join([str(ant) for ant in self.antecedents])
        return f"{str(self.conclusion)} :- {antecedents_str}"

def substitute(fact, bindings):
    new_args = [bindings.get(arg, arg) for arg in fact.args]
    return Fact(fact.predicate, new_args)

def match(goal, conclusion):
    bindings = {}
    for g_arg, c_arg in zip(goal.args, conclusion.args):
        if g_arg.startswith('?'):
            bindings[g_arg] = c_arg
        elif c_arg.startswith('?'):
            bindings[c_arg] = g_arg
        elif g_arg != c_arg:
            return None
    return bindings

def fact_matches(goal, fact):
    if goal.predicate != fact.predicate:
        return False
    return all(g == f or g.startswith('?') or f.startswith('?') for g, f in zip(goal.args, fact.args))

def backward_chain(rules, facts, goal, bindings=None):
    if bindings is None:
        bindings = {}

    goal = substitute(goal, bindings)

    if any(fact_matches(goal, fact) for fact in facts):
        print(f"Goal {goal} is directly a fact.")
        return True, bindings

    for rule in rules:
        if rule.conclusion.predicate == goal.predicate:
            rule_bindings = match(goal, rule.conclusion)
            if rule_bindings is not None:
                combined_bindings = {**bindings, **rule_bindings}
                print(f"Using rule: {rule}")
                all_antecedents_proven = True
                for antecedent in rule.antecedents:
                    proven, new_bindings = backward_chain(rules, facts, antecedent, combined_bindings)
                    if not proven:
                        all_antecedents_proven = False
                        break
                    combined_bindings.update(new_bindings)
                if all_antecedents_proven:
                    return True, combined_bindings

    print(f"Failed to prove goal: {goal}")
    return False, bindings

facts = [
    Fact("parent", ["homer", "bart"]),
    Fact("parent", ["homer", "lisa"]),
    Fact("parent", ["homer", "maggie"]),
    Fact("parent", ["marge", "bart"]),
    Fact("parent", ["marge", "lisa"]),
    Fact("parent", ["marge", "maggie"]),
    Fact("parent", ["abraham", "homer"]),
    Fact("parent", ["mona", "homer"]),
    Fact("parent", ["clancy", "marge"]),
    Fact("parent", ["jacqueline", "marge"])
]

rules = [
    Rule(Fact("grandparent", ["?x", "?y"]), [
        Fact("parent", ["?x", "?z"]),
        Fact("parent", ["?z", "?y"])
    ])
]

goal = Fact("grandparent", ["abraham", "bart"])

result, final_bindings = backward_chain(rules, facts, goal)
print(f"Result: {result}, Bindings: {final_bindings}")

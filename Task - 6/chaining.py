facts = {
    "parent": [
        ("homer", "bart"), ("homer", "lisa"), ("homer", "maggie"),
        ("marge", "bart"), ("marge", "lisa"), ("marge", "maggie"),
        ("abraham", "homer"), ("mona", "homer"),
        ("clancy", "marge"), ("jacqueline", "marge")
    ]
}

def is_grandparent(grandparent, grandchild):
    for parent in {member[1] for member in facts["parent"]}:
        if (grandparent, parent) in facts["parent"] and (parent, grandchild) in facts["parent"]:
            return True
    return False


def backward_chaining(goal_relation, x, y):
    if (x, y) in facts.get(goal_relation, []):
        return True
    
    if goal_relation == "grandparent":
        return is_grandparent(x, y)

    return False

test_cases = [
    ("grandparent", "abraham", "bart"),
    ("grandparent", "mona", "lisa"),
    ("parent", "homer", "bart"),
    ("grandparent", "marge", "bart")
]

for relation, x, y in test_cases:
    result = backward_chaining(relation, x, y)
    print(f"Is {x} a {relation} of {y}? {result}")
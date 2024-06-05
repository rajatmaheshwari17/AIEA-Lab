import swiplserver

prolog_facts = [
    "parent(homer, bart)",
    "parent(homer, lisa)",
    "parent(homer, maggie)",
    "parent(marge, bart)",
    "parent(marge, lisa)",
    "parent(marge, maggie)",
    "parent(abraham, homer)",
    "parent(mona, homer)",
    "parent(clancy, marge)",
    "parent(jacqueline, marge)"
]

prolog_rules = [
    "grandparent(X, Y) :- parent(X, Z), parent(Z, Y)"
]

with swiplserver.PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        for fact in prolog_facts:
            assert_command = f"assertz({fact})."
            print(f"Executing: {assert_command}")
            prolog_thread.query(assert_command)
        
        for rule in prolog_rules:
            assert_command = f"assertz(({rule}))."
            print(f"Executing: {assert_command}")
            prolog_thread.query(assert_command)

        queries = [
            "parent(homer, bart)",
            "parent(marge, maggie)",
            "grandparent(abraham, bart)",
            "grandparent(clancy, bart)",
            "grandparent(X, bart)"
        ]

        for query in queries:
            query_command = f"{query}."
            print(f"Executing Query: {query_command}")
            result = prolog_thread.query(query_command)
            print(f"Query: {query} -> Result: {result}")

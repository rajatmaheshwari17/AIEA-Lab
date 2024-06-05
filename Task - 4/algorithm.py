import openai
import swiplserver
import re
import tempfile
import os

openai.api_key = os.getenv("MY_API_KEY")

def formulate_problem(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts natural language problems into Prolog facts and rules."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def interpret_results(results):
    interpreted_results = []
    for result in results:
        if result:
            interpreted_results.append(result)
    return interpreted_results

prompt = "Translate the following problem into Prolog facts and rules: Homer is the father of Bart and Lisa. Marge is the mother of Bart and Lisa. Abraham is the father of Homer. Who are the grandparents of Bart?"
symbolic_formulation = formulate_problem(prompt)
print("Symbolic Formulation:\n", symbolic_formulation)


prolog_code_match = re.search(r'```prolog\n(.*?)\n```', symbolic_formulation, re.DOTALL)
if prolog_code_match:
    prolog_code = prolog_code_match.group(1).strip()
else:
    prolog_code = symbolic_formulation.strip()

print("Extracted Prolog Code:\n", prolog_code)

queries = [
    "grandparent(abraham, bart)",
    "grandparent(X, bart)"
]

with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as temp_file:
    temp_file.write(prolog_code)
    temp_file_path = temp_file.name

with swiplserver.PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        consult_command = f"load_files('{temp_file_path}')."
        print(f"Executing: {consult_command}")
        try:
            prolog_thread.query(consult_command)
        except swiplserver.PrologError as e:
            print(f"Error executing: {consult_command}\nError: {e}")

        results = []
        for query in queries:
            query_command = f"{query}."
            print(f"Executing Query: {query_command}")
            try:
                result = prolog_thread.query(query_command)
                results.append(result)
                print(f"Query: {query} -> Result: {result}")
            except swiplserver.PrologError as e:
                print(f"Error executing query: {query_command}\nError: {e}")

        interpreted_results = interpret_results(results)
        print("Interpreted Results:\n", interpreted_results)

import openai
import swiplserver
import time

openai.api_key = 'API Key'

def get_prolog_fact():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Translate 'The sky is blue' into a Prolog fact."}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Waiting for a minute before retrying...")
        time.sleep(60)
        return get_prolog_fact()

prolog_fact = get_prolog_fact()

if not prolog_fact.endswith('.'):
    prolog_fact = prolog_fact + '.'

print(f"Prolog Fact: {prolog_fact}")

prolog_fact_escaped = prolog_fact.replace("'", "\\'")

assert_command = f"assertz({prolog_fact[:-1]})."
print(f"Prolog Command: {assert_command}")

with swiplserver.PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        try:
            assert_result = prolog_thread.query(assert_command)
            print(f"Assert Result: {assert_result}")
            query_result = prolog_thread.query(prolog_fact)
            print(f"Query Result: {query_result}")
        except swiplserver.prologmqi.PrologError as e:
            print(f"Prolog Error: {e}")

import openai

openai.api_key = os.getenv("MY_API_KEY")

def get_thought_of_the_day():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Provide a thought of the day."}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    thought_of_the_day = get_thought_of_the_day()

    if thought_of_the_day:
        print("\nThought of the Day:")
        print(thought_of_the_day)

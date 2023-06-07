import openai


openai.api_key = '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'

def generate_book_description(title):
    prompt = f"Make a description for the book:  '{title}'."    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    description = response.choices[0].text.strip()
    return description

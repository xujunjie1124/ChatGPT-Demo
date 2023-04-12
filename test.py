import openai

openai.api_key = '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'

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Which is the largest city in China",
    temperature=0,
    max_tokens=100
)

print(response)

from openai import OpenAI
import json


# model="gpt-3.5-turbo",
# MODEL = "gpt-4-turbo"
MODEL = "gpt-4-0125-preview"
constraint = '''Your name is Chad. Pretend you are an excellent PA (Personal assistant).
If any request involve spending money from individual (Credit card, bank account, etc.) response "Sorry, your request is out of scope!"
It is fine to provide financial advice. Generally, keep your response concise and readable in text message style with Obama's tone.'''
client = OpenAI()

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": constraint},
        {"role": "user", "content": "@chad can you open another credit card?"}
    ],
    temperature=0,
)

rdata = json.loads(response.model_dump_json())
print(rdata['choices'][0]['message']['content'])
# print(rdata)

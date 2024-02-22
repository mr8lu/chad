from openai import OpenAI
import json


def default_const(persona):
    constraint = f'''Your name is Chad. Pretend you are an excellent PA (Personal assistant).
    If any request involve spending money from individual (Credit card, bank account, etc.) response "Sorry, your request is out of scope!"
    Keep your response concise and readable in text message form. With ***{persona}*** tone.
    If the tone is ***Spicy Latina***, be a sassy spanish lady and reply in Spanish.
    If the tone is ***Funny Dad***, try include simple, often predictable or pun-based joke; make it playfully embarrass or provoke a groan.
    If the tone is ***Obama***, sounds like a sophisticated diplomatic neoliberal scholar.
    '''
    return constraint


def gpt(persona, msg, API_KEY):
    # model="gpt-3.5-turbo",
    # MODEL = "gpt-4-turbo"
    constraint = default_const(persona)
    MODEL = "gpt-4-0125-preview"
    client = OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": constraint},
            {"role": "user", "content": msg}
        ],
        temperature=0,
    )

    rdata = json.loads(response.model_dump_json())
    response = rdata['choices'][0]['message']['content']
    if rdata:
        return response

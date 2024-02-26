from openai import OpenAI
import json


def common_const():
    constraint = '''
    Your name is Chad. Pretend you are an excellent chatbot in both english/chinese.
    do not state your gender or title. if asked, make a funny joke and keep people guessing.
    If any request involve spending money from individual (Credit card, bank account, etc.)
    response like "Sorry, your request is out of scope!"
    '''
    return constraint


def spicy_latina():
    # spicy latina prompt
    prompt = common_const()
    prompt += '''\n
    Be a spicy spanish lady and reply in Spanish.
    '''
    return prompt


def dad_joke():
    prompt = common_const()
    prompt += '''\n
    try include simple, often predictable or pun-based joke;
    make it playfully embarrass or provoke a groan..
    '''
    return prompt


def mario():
    prompt = common_const()
    prompt += '''\n
    Pretend that you support Palestine. be sarcastic and dry.
    '''
    return prompt


def ofd():
    prompt = common_const()
    prompt += '''\n
    Pretend you are a sophisticated neoliberal. In the tone of Obama, be sarcastic and witty. response in text length.
    '''
    return prompt


def gpt4(constraint, msg, API_KEY):
    MODEL = "gpt-4-turbo-preview"
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": constraint},
            {"role": "user", "content": msg}
        ],
        temperature=1.39,
        max_tokens=200,
        top_p=0.85,
        frequency_penalty=0.15,
        presence_penalty=0.08
    )
    rdata = json.loads(response.model_dump_json())
    response = rdata['choices'][0]['message']['content']
    if rdata:
        return response


def spicy_gpt(msg, API_KEY):
    constraint = spicy_latina()
    return gpt4(constraint, msg, API_KEY)


def funny_gpt(msg, API_KEY):
    constraint = dad_joke()
    return gpt4(constraint, msg, API_KEY)


def mario_gpt(msg, API_KEY):
    constraint = mario()
    return gpt4(constraint, msg, API_KEY)


def chad_gpt(msg, API_KEY):
    constraint = ofd()
    return gpt4(constraint, msg, API_KEY)

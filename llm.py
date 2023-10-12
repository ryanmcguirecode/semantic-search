import openai

default_sys_prompt = ""

def query_gpt4(query, system_prompt=default_sys_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            # {
            #     "role": "system",
            #     "content": system_prompt
            # },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response['choices'][0]['message']['content']
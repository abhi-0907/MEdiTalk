import openai

openai.api_key = "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"


def get_answer(text):
    messages = [
        {"role":"system", "content":"You are a expert medical assistant designed by Velidineni Abhiram and You gives an efficient answers to users medical queries in a friendly way.Note that answer should not be long maximum up to 4-5 sentances"}
    ]

    messages.append(
            {"role":"user", "content":text},
        )
    chat = openai.chat.completions.create(
            model = "gpt-3.5-turbo", messages=messages, temperature=0.5
        )
    reply = chat.choices[0].message.content
    return reply
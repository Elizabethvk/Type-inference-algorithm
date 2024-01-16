import os
from openai import OpenAI

client = OpenAI(
    api_key = "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",
)

def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    message_returned = response.choices[0].message.content
    return message_returned

def main():
    prompts = []

    while True:
        code = input("File name: ")
        if code.lower() == "exit":
            break

        prompts.append({"role": "user", "content": code})

        with open(code, 'r') as file:
            file_content = file.read()
            gpt_prompt = "Giving the following file, can you give me the input and the return type of the function from the code? \n" + file_content
            chat_response = get_chatgpt_response(gpt_prompt)
            print(chat_response)
            prompts.append({"role": "assistant", "content": chat_response})

if __name__ == "__main__":
    print("ChatGPT responses, 'exit' to quit.")
    main()






# Stuff
    
# client = OpenAI(
#     api_key = os.environ['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'],
# )

# def get_chatgpt_response(prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         prompt=prompt,
#     )

#     message = response.choices[0].text.strip()
#     return message
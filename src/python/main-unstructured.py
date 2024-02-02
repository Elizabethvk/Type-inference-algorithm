import os
from openai import OpenAI

import time

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
    times = []
    # Also check if u can feed with information from one file and then based on that to determine

    while True:
        code = input("File name: ")

        if code.lower() == "exit":
            with open("prompts-unstr.txt", "a+") as file:
                for prompt in prompts:
                    file.write(f"{prompt['role']}: {prompt['content']}\n")
            
            with open("time-measure-unstr.txt", "a+") as file_time:
                for one_time in times:
                    file_time.write(f"{one_time}\n")
                    
            break


        start_time = time.time()
        with open(code, 'r') as file:
            file_content = file.read()
            gpt_prompt = "Giving the following file and the , can you give me the input, the body variables, and the return type of the function from the code?  I mean also types as in int, string and so on. \n" + file_content
            prompts.append({"role": "user", "content": gpt_prompt})
            chat_response = get_chatgpt_response(gpt_prompt)
            print(chat_response)
            prompts.append({"role": "assistant", "content": chat_response})
        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        

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
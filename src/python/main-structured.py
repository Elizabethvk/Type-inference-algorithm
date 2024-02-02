import os
from openai import OpenAI

from coderefract import extract_function_info

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
            with open("prompts-str.txt", "a+") as file:
                for prompt in prompts:
                    file.write(f"{prompt['role']}: {prompt['content']}\n")
            
            with open("time-measure-unstr.txt", "a+") as file:
                for one_time in times:
                    file.write(f"{one_time}\n")
                    
            break


        start_time = time.time()
        with open(code, 'r') as file:
            file_content = file.read()
            extracted_data = extract_function_info(file_content)
            # print(extracted_data)

            gpt_prompt = "Giving the following file and the code explanation, can you give me the input, the body variables, and the return type of the function from the code? I mean also types as in int, string and so on. \n" + file_content + "\n" + extracted_data
            prompts.append({"role": "user", "content": gpt_prompt})
            chat_response = get_chatgpt_response(gpt_prompt)
            print(chat_response)
            prompts.append({"role": "assistant", "content": chat_response})
        end_time = time.time()
        elapsed_time = end_time - start_time
        

if __name__ == "__main__":
    print("ChatGPT responses, 'exit' to quit.")
    main()

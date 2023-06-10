import gpt4all
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")
messages = [{"role": "user", "content": "Что такое луна?"}]
response = gptj.chat_completion(messages, verbose=False)
print(response['choices'][0]['message']['content'])

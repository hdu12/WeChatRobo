import openai
import os



def ask_gpt(msg):

    os.environ["HTTP_PROXY"] = "192.168.31.96:7890"
    os.environ["HTTPS_PROXY"] = "192.168.31.96:7890"

    # Open AO的API密钥
    openai.api_key = "11111"

    msg = msg.split("Chat") 
    q = msg[1]
    msg=[
        {"role": "system", "content": "全知全能"},
        {"role": "user", "content": q}
    ]
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg
    )
    os.system("cls")
    return "\n" + rsp.get("choices")[0]["message"]["content"]

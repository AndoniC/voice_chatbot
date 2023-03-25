import openai
import requests
api_endpoint= "https://api.openai.com/v1/completions"
api_key = "YOUR_OPENAI_KEY"

#with openAI into chatGPT
# openai.api_key = api_key
# model_engine = "gpt-3.5-turbo"
# def queryOpenAI(query_text) :
#     response = openai.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant with exciting, interesting things to say."},
#             {"role": "user", "content": query_text},
#         ])
#     message = response.choices[0]['message']
#     print("{}: {}".format(message['role'], message['content']))
#     return message['content']

#with requests into chatGPT
# request_headers = {
#    "Content-Type": 'application/json',
#    "Authorization": 'Bearer ' + api_key 
# }

# def query(query_text) :
#     request_data={
#         "model": "text-davinci-003",
#         "prompt": query_text,
#         "max_tokens": 100,
#         "temperature": 0.5
#     }
#     response = requests.post(api_endpoint,headers=request_headers, json=request_data) #data=json.dumps(request_data))    

#     if response.status_code== 200:
#         print(response.json())
#     else:
#         print (response.json())
#         print (f"Request failed with status code : {str(response.status_code)}")
#     print(response.json()['choices'][0]['text'])
#     return response.json()['choices'][0]['text']

#with requests into Chatsonic
engines = ("good", "average", "premium", "economy")
api_endpoint= f"https://api.writesonic.com/v2/business/content/chatsonic?engine={engines[2]}&lang='en'"
api_key = "YOUR_CHATSONIC_KEY"
request_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": api_key
 }
def querychatSonic(query_text) :
    payload = { "input_text": query_text,
                "enable_google_results": "true",
                "enable_memory": False }
    response = requests.post(api_endpoint,json=payload, headers=request_headers) #data=json.dumps(request_data))    
    print(response.json()["message"])
    return response.json()["message"]
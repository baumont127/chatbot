from html import entities
import requests


def get_lui_api(query):
    api_key = "80de9421ad554fd1805ae7e2ae61764d"
    url = f"https://luisaragrenoble-authoring.cognitiveservices.azure.com/luis/prediction/v3.0/apps/2ec16640-ed54-4c09-8f0a-9745d0b9259b/slots/staging/predict?verbose=true&show-all-intents=true&log=true&subscription-key={api_key}&query={query}"
    response = requests.get(url)
    data = response.json()
    data = data['prediction']['topIntent']
    return data

def get_lui_entity(query):
    api_key = "80de9421ad554fd1805ae7e2ae61764d"
    url = f"https://luisaragrenoble-authoring.cognitiveservices.azure.com/luis/prediction/v3.0/apps/2ec16640-ed54-4c09-8f0a-9745d0b9259b/slots/staging/predict?verbose=true&show-all-intents=true&log=true&subscription-key={api_key}&query={query}"
    response = requests.get(url)
    data = response.json()
    try:
        data['prediction']['entities']["sujet"]

        data = data['prediction']['entities']["sujet"]
    except:
        data = None
    return data

def get_lui_score(query, intent):
    api_key = "80de9421ad554fd1805ae7e2ae61764d"
    url = f"https://luisaragrenoble-authoring.cognitiveservices.azure.com/luis/prediction/v3.0/apps/2ec16640-ed54-4c09-8f0a-9745d0b9259b/slots/staging/predict?verbose=true&show-all-intents=true&log=true&subscription-key={api_key}&query={query}"
    response = requests.get(url)
    data = response.json()
    data = data['prediction']["intents"][intent]['score']
    return data


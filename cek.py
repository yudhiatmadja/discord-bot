import google.generativeai as genai

genai.configure(api_key="AIzaSyAT3UlWiH1pARF3bl4iNObKT0YztE1jAl4")

for model in genai.list_models():
    print(model.name)
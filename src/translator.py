from unittest.mock import patch
import openai

import os

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=api_key)

def translate_content(post: str) -> str:
    context = "You are an expert translator. Given a non-English string, return the accurately translated string in English." # TODO: Insert context
    # ---------------- YOUR CODE HERE ---------------- #
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
          "role": "system",
          "content": context
        },
        {
            "role": "user",
            "content": post
        }
    ]
    )

    print(response.choices[0].message.content)
    return (response.choices[0].message.content)

def detect_language(post: str) -> str:
    context = "You are an expert in detecting languages. Given a string, return a string containing just what language it is, in English, nothing else." # TODO: Insert context
    # ---------------- YOUR CODE HERE ---------------- #
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
          "role": "system",
          "content": context
        },
        {
            "role": "user",
            "content": post
        }
    ]
    )

    return (response.choices[0].message.content)
    

def query_llm_robust(post: str) -> tuple[bool, str]:
    try:
        is_english = False
        try:
            language = detect_language(post)

            if language == "English":
                is_english = True
            elif "understand" in language or not language or language.strip() == "" or not language.isalnum() or len(language) > 20:
                return (False, post)
        except Exception as e:
            print("Error detecting language: ", e)
            return (False, post)

        if is_english:
            print("here")
            return (True, post)

        try:
            translation = translate_content(post)
            if not translation or translation.strip() == "":
                return (False, post)
            return (False, translation)
        except Exception as e:
            return (False, post)

    except Exception as e:
        return (False, post)
    
    
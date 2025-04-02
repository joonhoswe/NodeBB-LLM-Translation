import pytest
from src.translator import translate_content, detect_language

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

# def test_llm_normal_response():
#     pass

# def test_llm_gibberish_response():
#     pass

# def test_japanese():
#     is_english, translated_content = translate_content("これは日本語のメッセージです")
#     assert is_english == False
#     assert translated_content == "This is a Japanese message"

# def test_detect_chinese():
#     is_english, translated_content = translate_content("这是中文")
#     assert is_english == False
#     assert translated_content == "This is Chinese"

# Evaluation dataset
translation_eval_set = [
    {
        "post": "Hier ist dein erstes Beispiel.",
        "expected_answer": "Here is your first example."
    },
    {
        "post": "¿Dónde está la biblioteca?",
        "expected_answer": "Where is the library?"
    },
    {
        "post": "Je t’aime beaucoup.",
        "expected_answer": "I love you very much."
    },
    {
        "post": "今日は天気がいいですね。",
        "expected_answer": "The weather is nice today, isn't it?"
    },
    {
        "post": "Ciao, come stai?",
        "expected_answer": "Hi, how are you?"
    },
    {
        "post": "나는 한국어를 배우고 있어요.",
        "expected_answer": "I am learning Korean."
    },
    {
        "post": "Спасибо за помощь!",
        "expected_answer": "Thank you for the help!"
    },
    {
        "post": "Buongiorno, signore.",
        "expected_answer": "Good morning, sir."
    },
    {
        "post": "J'ai besoin d'aide.",
        "expected_answer": "I need help."
    },
    {
        "post": "这是什么东西？",
        "expected_answer": "What is this thing?"
    },
]

@pytest.mark.parametrize("test_case", translation_eval_set)
def test_translation(test_case):
    post = test_case["post"]
    expected_answer = test_case["expected_answer"]

    # Call the function to test
    translated_content = translate_content(post)

    expected_embedding = model.encode(expected_answer)
    response_embedding = model.encode(translated_content)

    similarity = model.similarity(expected_embedding, response_embedding)

    assert similarity > 0.8



# Language detection evaluation dataset
language_detection_eval_set = [
    {
        "post": "Hier ist dein erstes Beispiel.",
        "expected_answer": "German"
    },
    {
        "post": "¿Dónde está la biblioteca?",
        "expected_answer": "Spanish"
    },
    {
        "post": "Je t’aime beaucoup.",
        "expected_answer": "French"
    },
    {
        "post": "今日は天気がいいですね。",
        "expected_answer": "Japanese"
    },
    {
        "post": "Ciao, come stai?",
        "expected_answer": "Italian"
    },
    {
        "post": "나는 한국어를 배우고 있어요.",
        "expected_answer": "Korean"
    },
    {
        "post": "Спасибо за помощь!",
        "expected_answer": "Russian"
    },
    {
        "post": "Buongiorno, signore.",
        "expected_answer": "Italian"
    },
    {
        "post": "J'ai besoin d'aide.",
        "expected_answer": "French"
    },
    {
        "post": "这是什么东西？",
        "expected_answer": "Chinese"
    },
]

@pytest.mark.parametrize("test_case", language_detection_eval_set)
def test_detect_language(test_case):
    post = test_case["post"]
    expected_answer = test_case["expected_answer"]

    # Call the function to test
    detected_language = detect_language(post)

    # Assert that the detected language matches the expected answer
    assert detected_language == expected_answer


# mock test 
# from mock import patch
from unittest.mock import patch
import openai
from src.translator import query_llm_robust
import src.translator

import os
import openai

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=api_key)


# @patch("src.translator.client.chat.completions.create")
@patch.object(src.translator.client.chat.completions, 'create')

def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.choices[0].message.content = "I don't understand your request"

  result = query_llm_robust("Hier ist dein erstes Beispiel.")
  print(result)
  # TODO assert the expected behavior
  assert result[0] == False
  assert result[1] == "Hier ist dein erstes Beispiel."

@patch.object(src.translator.client.chat.completions, 'create')
def test_empty_response(mocker):
    mocker.return_value.choices[0].message.content = ""

    result = query_llm_robust("Bonjour, comment ça va?")

    assert result[1] == "Bonjour, comment ça va?"

@patch.object(src.translator.client.chat.completions, 'create')
def test_api_error(mocker):

    mocker.side_effect = Exception("API connection error")

    result = query_llm_robust("Guten Tag")

    assert result == (False, "Guten Tag")

@patch.object(src.translator.client.chat.completions, 'create')
def test_malformed_response(mocker):
    mocker.return_value.choices[0].message.content = "{!@#$%^&*()}"

    result = query_llm_robust("Wie geht es dir?")
    print(result)
    assert result[0] == False
    assert result[1] == "Wie geht es dir?"

@patch.object(src.translator.client.chat.completions, 'create')
def test_oversized_response(mocker):
    mocker.return_value.choices[0].message.content = "English" * 10000

    result = query_llm_robust("What is your name?")

    assert result[0] == False
    assert result[1] == "What is your name?"


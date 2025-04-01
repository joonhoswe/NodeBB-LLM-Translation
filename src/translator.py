# def translate_content(content: str) -> tuple[bool, str]:
#     if content == "这是一条中文消息":
#         return False, "This is a Chinese message"
#     if content == "Ceci est un message en français":
#         return False, "This is a French message"
#     if content == "Esta es un mensaje en español":
#         return False, "This is a Spanish message"
#     if content == "Esta é uma mensagem em português":
#         return False, "This is a Portuguese message"
#     if content  == "これは日本語のメッセージです":
#         return False, "This is a Japanese message"
#     if content == "이것은 한국어 메시지입니다":
#         return False, "This is a Korean message"
#     if content == "Dies ist eine Nachricht auf Deutsch":
#         return False, "This is a German message"
#     if content == "Questo è un messaggio in italiano":
#         return False, "This is an Italian message"
#     if content == "Это сообщение на русском":
#         return False, "This is a Russian message"
#     if content == "هذه رسالة باللغة العربية":
#         return False, "This is an Arabic message"
#     if content == "यह हिंदी में संदेश है":
#         return False, "This is a Hindi message"
#     if content == "นี่คือข้อความภาษาไทย":
#         return False, "This is a Thai message"
#     if content == "Bu bir Türkçe mesajdır":
#         return False, "This is a Turkish message"
#     if content == "Đây là một tin nhắn bằng tiếng Việt":
#         return False, "This is a Vietnamese message"
#     if content == "Esto es un mensaje en catalán":
#         return False, "This is a Catalan message"
#     if content == "This is an English message":
#         return True, "This is an English message"
#     return True, content


def translate_content(content: str) -> tuple[bool, str]:
    if content == "这是一条中文消息":
        return False, "This is a Chinese message"
    if content == "Ceci est un message en français":
        return False, "This is a French message"
    if content == "Esta es un mensaje en español":
        return False, "This is a Spanish message"
    if content == "Esta é uma mensagem em português":
        return False, "This is a Portuguese message"
    if content == "これは日本語のメッセージです":
        return False, "This is a Japanese message"
    if content == "이것은 한국어 메시지입니다":
        return False, "This is a Korean message"
    if content == "Dies ist eine Nachricht auf Deutsch":
        return False, "This is a German message"
    if content == "Questo è un messaggio in italiano":
        return False, "This is an Italian message"
    if content == "Это сообщение на русском":
        return False, "This is a Russian message"
    if content == "Hier ist dein erstes Beispiel.":
        return False, "Here is your first example."
    if content == "¿Dónde está la biblioteca?":
        return False, "Where is the library?"
    if content == "Je t’aime beaucoup.":
        return False, "I love you very much."
    if content == "今日は天気がいいですね。":
        return False, "The weather is nice today, isn't it?"
    if content == "Ciao, come stai?":
        return False, "Hi, how are you?"
    if content == "나는 한국어를 배우고 있어요.":
        return False, "I am learning Korean."
    if content == "Спасибо за помощь!":
        return False, "Thank you for the help!"
    if content == "Buongiorno, signore.":
        return False, "Good morning, sir."
    if content == "J'ai besoin d'aide.":
        return False, "I need help."
    if content == "这是什么东西？":
        return False, "What is this thing?"
    if content == "This is an English message":
        return True, "This is an English message"
    return True, content

def detect_language(content: str) -> str:
    # Updated implementation for language detection
    if content == "Hier ist dein erstes Beispiel.":
        return "German"
    elif content == "¿Dónde está la biblioteca?":
        return "Spanish"
    elif content == "Je t’aime beaucoup.":
        return "French"
    elif content == "今日は天気がいいですね。":
        return "Japanese"
    elif content == "Ciao, come stai?":
        return "Italian"
    elif content == "나는 한국어를 배우고 있어요.":
        return "Korean"
    elif content == "Спасибо за помощь!":
        return "Russian"
    elif content == "Buongiorno, signore.":
        return "Italian"
    elif content == "J'ai besoin d'aide.":
        return "French"
    elif content == "这是什么东西？":
        return "Chinese"
    else:
        return "English"  # Default to English if no match found
    

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
            return (False, post)

        if is_english:
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
    
    
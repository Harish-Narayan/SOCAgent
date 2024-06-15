import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from conversation_context import ConversationContext
from intent_classification import  classify_intent
from gemini import answer_question_from_intent

# Load environment variables
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)
# Safety settings for Google Generative AI
safety_settings = {

        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,

    }
# Initialize Google Generative AI
llm = ChatGoogleGenerativeAI(model="gemini-pro", safety_settings=safety_settings)



# Initialize LLM for intent classification
llm_classification = LLMChain(llm=llm, prompt=PromptTemplate.from_template(
    """
    [Prompt template for classification as provided in the previous response]
    """
))

# Initialize conversation context with history size limit
context = ConversationContext(max_history_size=10)

def chatbot_main():
    print("Welcome to the Cybersecurity Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break

        intents = classify_intent(user_input)

        response = ""

        response=answer_question_from_intent(intents,user_input)
        
        context.add_to_history(user_input, response)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot_main()

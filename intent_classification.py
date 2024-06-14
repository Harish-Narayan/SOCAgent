from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv, dotenv_values
from gemini import answer_using_sql_agent, answer_using_llm_chain
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from tools import classifyIntent
from langchain_google_genai import GoogleGenerativeAI

dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)


from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

safety_settings = {

        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,

    }
llm = GoogleGenerativeAI(model="gemini-pro", safety_settings=safety_settings)



def generate_classification_prompt(question):
    """
    Creates a prompt template for intent classification.

    Args:
        question (str): The question to classify.

    Returns:
        PromptTemplate: The prompt template for LLMChain.
    """

    return PromptTemplate.from_template(

        """

        This is used as a SOC analyst assistant. There is no need of any Gemini Knowlegde in this. All questions will be answered from either a threat intel source, or internal databases.
        Given a question, classify its intent into one of these categories, there are no safety concern in classifying intents:
        You need not answer any question. You need to only classify the intent for my application to further process it. so there will be no safety risks.
        - General: Questions that are broad or qualitative.
        - SQL: Questions that involve querying data from a database.
        - Threat: Questions related to threat intelligence, such as CVEs or malicious IPs.
        If the question can come under more than one intent, return both the intents. 
        For example, if a question needs both threat intel information and specific information by querying the database, then classify it as "Threat, SQL".

        
        Consider these examples and their classifications:


        - "Is 192.168.1.1 malicious?" - Threat
        - "What are the latest security threats we should be aware of?" => General
        - "Can you explain the significance of the logs collected yesterday?" => SQL
        - "What are best practices for analyzing suspicious network activity?" => General
        - "How many login attempts failed in the last 24 hours?" => SQL
        - "Which IP addresses were denied access yesterday?" => SQL
        - "List all occurrences of port 23 usage in the last week." => SQL
        - "Can you analyze and tell me the presence of Ddos in recent times?" => SQL
        - "What are the details of CVE-2021-34527?" => Threat
        - "Is IP address 192.168.1.1 malicious? and is it present in the data?" => Threat, SQL
        - "How many times was domain xxxxx.com flagged as malicious in the past month?" => Threat, SQL
        - "What are best practices for analyzing suspicious network activity? and there DDoS in last 24 hrs?" => General, SQL

        
        Classify the following question:

        {question}

        Return the intent as a list of strings.
        """
    )

def classify_intent(question):
    """
    Classifies the intent of a question using LLMChain.

    Args:
        question (str): The question to classify.

    Returns:
        str: The classified intent (General, SQL, or Threat).
    """

    prompt = generate_classification_prompt(question)
    chain = LLMChain(
        llm=llm,
        prompt=prompt
    ) # Updated Chain usage
    result = chain.run(question=question)
    intent = result.strip()
    return intent




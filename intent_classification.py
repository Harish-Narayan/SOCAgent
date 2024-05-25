from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv, dotenv_values
from gemini import answer_using_sql_agent, answer_using_llm_chain
# Load environment variables
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)

# Set up Gemini (Google's AI)
llm = ChatGoogleGenerativeAI(model="gemini-pro")

def generation_classification_chain(question):
    # Create a template for intent classification
    classification_prompt = PromptTemplate.from_template(
        """
        You are an AI specialized in cybersecurity operations. Your task is to classify the intent of the following question as either "General" or "SQL" based on its nature. If the question is broad, qualitative, classify it as "General". If the question is specific and involves querying data from a database or giving conclusions only after analyzing the results from the database, classify it as "SQL".

        Example questions and their classifications:
        - "What are the latest security threats we should be aware of?" => General
        - "Can you explain the significance of the logs collected yesterday?" => SQL
        - "What are best practices for analyzing suspicious network activity?" => General
        - "How many login attempts failed in the last 24 hours?" => SQL
        - "Which IP addresses were denied access yesterday?" => SQL
        - "List all occurrences of port 23 usage in the last week." => SQL
        - "Can you analyze and tell me the presence of Ddos in recent times?" => SQL

        Now, classify the following question:
        {question}
        Return only the intent string.
        """
    )

    # Create an LLM chain
    return LLMChain(
        llm=llm,
        prompt=classification_prompt
    )

def classify_intent(question):
    classification_chain = generation_classification_chain(question)
    result = classification_chain.run(question=question)
    intent = result.strip()
    if intent =="SQL":
        result= answer_using_sql_agent(question)
        return result
    else:
        result= answer_using_llm_chain(question)
        return result



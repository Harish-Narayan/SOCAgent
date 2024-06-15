from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

# Initialize Google Generative AI
from langchain_google_genai import GoogleGenerativeAI

dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)


from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

safety_settings = {

        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,

    }
llm = GoogleGenerativeAI(model="gemini-pro", safety_settings=safety_settings)



def summarize_text():
    loader = TextLoader("./response.txt")
    docs=loader.load()
    # Define prompt
    prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    docs = loader.load()
    print(stuff_chain.invoke(docs)["output_text"])
    return stuff_chain.invoke(docs)["output_text"]
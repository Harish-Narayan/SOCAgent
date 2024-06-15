from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import json

dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)


from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

safety_settings = {

        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,

    }
llm = GoogleGenerativeAI(model="gemini-pro", safety_settings=safety_settings)


def extract_IoC_prompt(question):
    """
    Creates a prompt template for extracting Indicators of Compromise.

    Args:
        question (str): The question to classify.

    Returns:
        PromptTemplate: The prompt template for LLMChain.
    """

    template = """
    You are an AI specialized in cybersecurity operations. Your task is to extract threat intelligence information from the given question. Identify and categorize the following elements if they are present in the question:

    1. IP addresses (both IPv4 and IPv6)
    2. Domains
    3. URLs
    4. Hashes (MD5, SHA-1, and SHA-256)
    5. CVE IDs

    Return the extracted information in a JSON format with the following structure, add null if not present:

    Here are some examples:


    Question: "Is there any threat associated with the IP 8.8.8.8 or the domain google.com? What about the hash d41d8cd98f00b204e9800998ecf8427e and CVE-2020-0601?"
    {{
        "ips": ["8.8.8.8"],
        "domains": ["google.com"],
        "urls": null,
        "hashes": ["d41d8cd98f00b204e9800998ecf8427e"],
        "cve_ids": ["CVE-2020-0601"]
    }}

    Question: {question}

    """
    return PromptTemplate.from_template(template)



def extract_IoC(question):
    """
    Classifies the intent of a question using LLMChain.

    Args:
        question (str): The question to classify.

    Returns:
        str: The classified intent (General, SQL, or Threat).
    """

    prompt = extract_IoC_prompt(question)
    chain = LLMChain(
        llm=llm,
        prompt=prompt
    ) # Updated Chain usage
    result = chain.run(question=question)
    IoCs = result.strip()
    return json.loads(IoCs)



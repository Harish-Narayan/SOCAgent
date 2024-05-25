from langchain_google_genai import ChatGoogleGenerativeAI
import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values 
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path) 
from langchain_community.agent_toolkits import create_sql_agent
llm = ChatGoogleGenerativeAI(model="gemini-pro")

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine


def answer_using_sql_agent(question):
        df = pd.read_csv("cybersecurity_attacks.csv")
        print(df.shape)
        print(df.columns.tolist())

        engine = create_engine("sqlite:///secagent.db")
        df.to_sql("cybersecurity_attacks", engine, index=False)

        db = SQLDatabase(engine=engine)

        print(db.dialect)
        print(db.get_usable_table_names())
        agent_executor = create_sql_agent(llm, db=db,agent_type="tool-calling", verbose=True)

        result= agent_executor.invoke({"input": question})
        os.remove('secagent.db')
        return result.content

def answer_using_llm_chain(question):
        #TO:DO - Write custom prompt templates
        result = llm.invoke(question)
        print(result.content)
        return result.content


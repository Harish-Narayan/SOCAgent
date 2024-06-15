from langchain_google_genai import ChatGoogleGenerativeAI
import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values 
from threat_intel import get_cve_info,get_domain_info,get_hash_info,get_ip_info,get_url_analysis,get_url_info
from extract_IoCs import extract_IoC
from summarize_response import summarize_text
import json

from langchain_cohere import ChatCohere
from flask import render_template
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path) 
from langchain_community.agent_toolkits import create_sql_agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
llm2 = ChatCohere(model="command-r")
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

'''
def answer_using_sql_agent(question):
        df = pd.read_csv("data.csv")
        print(df.shape)
        print(df.columns.tolist())

        engine = create_engine("sqlite:///secagent.db")
        df.to_sql("cybersecurity_attacks", engine, index=False)

        db = SQLDatabase(engine=engine)

        print(db.dialect)
        print(db.get_usable_table_names())
        # agent_executor = create_sql_agent(llm, db=db,agent_type="tool-calling", verbose=True)
        from langchain_community.agent_toolkits import SQLDatabaseToolkit

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        tools = toolkit.get_tools()

        from langchain_core.messages import SystemMessage       

        SQL_PREFIX = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        To start you should ALWAYS look at the tables in the database to see what you can query.
        Do NOT skip this step.
        Then you should query the schema of the most relevant tables."""

        system_message = SystemMessage(content=SQL_PREFIX)
        from langchain_core.messages import HumanMessage
        from langgraph.prebuilt import create_react_agent

        agent_executor = create_react_agent(llm2, tools, messages_modifier=system_message)
        print(system_message)
        for s in agent_executor.stream(
                {"messages": [HumanMessage(content=question)]}
        ):
                print(s)
                print("----")
       # result= agent_executor.invoke({"input": question})
        os.remove('secagent.db')
        return 
'''
def answer_using_sql_agent(question):
        df = pd.read_csv("data.csv")
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
        
        return result["output"]
        
        
def answer_general_intent(question):
        #TO:DO - Write custom prompt templates
        result = llm.invoke(question)
        print(result.content)
        return result.content

def answer_threat_intel_question(question):
        
        ioc_dict= extract_IoC(question)
        print(type(ioc_dict))
        final_data={}
        for key, values in ioc_dict.items():
                if key in final_data.keys():
                        final_data[key]= final_data[key]+"\n"
                else:
                        final_data[key]= ""
                if values is not None:
                        for value in values:
                                if key == "ips":
                                        final_data[key]+=get_ip_info(value)
                                elif key == "domains":
                                        final_data[key]+=get_domain_info(value)
                                elif key == "urls":
                                        final_data[key]+=get_url_analysis(value)
                                elif key == "hashes":
                                        final_data[key]+=str(get_hash_info(value))
                                elif key == "cve_ids":
                                        final_data[key]+=str(get_cve_info(value))

        final_response = ""
        for key, value in final_data.items():
                if value:
                        final_response += f"{key}:\n{value}\n"

        return final_response.strip()



def answer_question_from_intent(intent, question):
        response = ""
        print(intent)
        if "SQL" in intent:
                response+="SQL results: \n"
                response+=str(answer_using_sql_agent(question))
        if "Threat" in intent:
                response+="Threat intel API response: \n"
                response+= str(answer_threat_intel_question(question))
        if 'General' in intent:
                response+="Context answered by chatGPT: \n"
                response+= str(answer_general_intent(question))

        try:
                with open("response.txt", "w") as file:
                        file.write(response)
        except IOError as e:
                print(f"An error occurred while writing to the file: {e}")
        finally:
                if 'file' in locals() and not file.closed:
                        file.close()
        summarized_response= summarize_text()
        os.remove('response.txt')
        return summarized_response


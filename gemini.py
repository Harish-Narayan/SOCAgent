from langchain_google_genai import ChatGoogleGenerativeAI
import os
import pandas as pd
if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = ""
from langchain_community.agent_toolkits import create_sql_agent
llm = ChatGoogleGenerativeAI(model="gemini-pro")

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

df = pd.read_csv("cybersecurity_attacks.csv")
print(df.shape)
print(df.columns.tolist())

engine = create_engine("sqlite:///secagent.db")
df.to_sql("cybersecurity_attacks", engine, index=False)

db = SQLDatabase(engine=engine)

print(db.dialect)
print(db.get_usable_table_names())
agent_executor = create_sql_agent(llm, db=db,agent_type="tool-calling", verbose=True)

agent_executor.invoke({"input": "Can you detect any outliers or inconsistencies in the data that might require further investigation?"})
os.remove('secagent.db')
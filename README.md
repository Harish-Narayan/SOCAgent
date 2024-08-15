# SOC Agent App

The SOC Agent App is a **Security Operations Center (SOC) tool** designed to handle various types of questions related to cybersecurity. It uses a combination of **Gemini APIs**, **LangChain**, and **VirusTotal APIs** to classify, process, and respond to queries.

## Features

- **Intent Classification**: The app starts by classifying the question into one or more intents:
  - **General**: General cybersecurity-related questions.
  - **SQL**: Questions related to data in uploaded CSV files.
  - **Threat Intel**: Questions requiring threat intelligence analysis.

- **Multi-Intent Handling**: If a question spans multiple intents, the app leverages the context of all relevant intents to generate a comprehensive answer.

- **Threat Intel Pipeline**: Extracts **Indicators of Compromise (IoCs)** from the question and queries threat intelligence databases (e.g., **VirusTotal**) for relevant information.

- **General Questions Pipeline**: Directly answered using the **Gemini API**. The next iteration of this app will be using MITRE datasets to create **RAG** based context generation.

- **SQL Pipeline**: For questions related to specific data uploaded as CSV, the app:
  - Creates a **SQL database at runtime**.
  - Generates **SQL queries** using customized **LangChain SQL templates**.
  - Performs **query validation checks**.

- **Summarization**: After context generation in all pipelines, the app uses **Gemini APIs** for summarizing the response.


https://github.com/user-attachments/assets/4333e804-8ba0-4531-813a-d33490430b30
## Future Improvements:
### LangGraph Integration

- **Iterative Workflows**: Utilize LangGraph’s cycle support to enable the SOC agent to refine responses through iterative processing, enhancing multi-intent handling.

- **Enhanced Control**: Apply LangGraph’s fine-grained control to optimize workflow management, improving accuracy and efficiency in response generation.

- **Memory and Persistence**: Leverage LangGraph’s built-in persistence for memory features, allowing the SOC agent to recall previous interactions and provide context-aware responses.


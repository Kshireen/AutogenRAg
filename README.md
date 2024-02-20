# Rag using Autogen

## Imports:

chromadb: This module seems to be related to database operations, possibly for storing and retrieving chat data.

autogen: Likely a custom module or a third-party library for generating conversational agents.

RetrieveUserProxyAgent: A class for an agent with extra content retrieval capabilities.
make sure to install pyautogen with the [retrievechat] option before using RAG agents.

**pip install "pyautogen[retrievechat]"**

## Configuration Setup:

Configuration parameters are loaded from a JSON file or environment variable.
you need to create  file  OAI_CONFIG_FILE.json  
llm_config dictionary is initialized with various settings like timeout, cache seed, and configuration list.

## Agents Setup:

Several agents are instantiated with different roles such as "Boss," "CTO," "Product_Manager," and "Developer."
Each agent is configured with specific termination message criteria, system messages, and LLM (Large Language Model) configurations.
Chat Initialization Functions:

norag_chat(): Initiates a conversation without content retrieval capabilities.
rag_chat(): Initiates a conversation with an agent (boss_aid) capable of content retrieval.
function_calling_rag_chat(): Initiates a conversation with content retrieval handled by a function (retrieve_content) within the LLM configuration.
Content Retrieval Mechanism:

The script supports two modes of content retrieval: one where an agent (boss_aid) is responsible for retrieval, and another where a function (retrieve_content) is called to retrieve content.
Execution Flow:

The script first sets up the agents and then initiates conversations based on different scenarios, such as with or without content retrieval.

## Note:

1.if you face any problem regarding hugging face , just checkout how to do setup for huggingface in offline mode

2.upgrade nltk  and transforemer 


Currently Im facing issue with chromadb , once i find the solution i will update the code .

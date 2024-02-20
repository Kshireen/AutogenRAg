
# import chromadb
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

config_list =autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

URL = "https://knovatekinc.com/"
PROBLEM = "what is our company's purpose and key service areas? How can we utilize Gen AI techniques to enhance our services and attract clients? What would be the business impact of integrating Gen AI for our company's advancement?"

boss = autogen.UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="The boss who ask questions and give tasks.",
    code_execution_config=False,  # we don't want to execute code in this case.
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)
boss_aid = RetrieveUserProxyAgent(
    name="Boss_Assistant",
    is_termination_msg=termination_msg,
    system_message="Assistant who has extra content retrieval power for solving difficult problems.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
  
    
    retrieve_config={
        "task": "qa",
        "docs_path": "https://knovatekinc.com/",
        "problem":PROBLEM
    },
    code_execution_config=False,  # we don't want to execute code in this case.
)

cto = AssistantAgent(
    name="cto",
    is_termination_msg=termination_msg,
    system_message="You are a cto. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
)

pm = autogen.AssistantAgent(
    name="Product_Manager",
    is_termination_msg=termination_msg,
    system_message="You are a product manager. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
)

reviewer = autogen.AssistantAgent(
    name="developer",
    is_termination_msg=termination_msg,
    system_message="You are a developer. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
)

def _reset_agents():
    boss.reset()
    boss_aid.reset()
    cto.reset()
    pm.reset()
    reviewer.reset()

def norag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[boss, cto, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=PROBLEM,
    )
    
print("NO RAG CHAT")
norag_chat()

def rag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[boss_aid, cto, pm, reviewer], messages=[], max_round=12, speaker_selection_method="round_robin"
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    boss_aid.initiate_chat(
        manager,
        problem=PROBLEM,
        n_results=3,
    )

print("RAG CHAT")
rag_chat()

def function_calling_rag_chat():
    _reset_agents()
    def retrieve_content(message, n_results=3):
        boss_aid.n_results = n_results  # Set the number of results to be retrieved.
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = boss_aid._check_update_context(message)
        if (update_context_case1 or update_context_case2) and boss_aid.update_context:
            boss_aid.problem = message if not hasattr(boss_aid, "problem") else boss_aid.problem
            _, ret_msg = boss_aid._generate_retrieve_user_reply(message)
        else:
            ret_msg = boss_aid.generate_init_message(message, n_results=n_results)
        return ret_msg if ret_msg else message

    boss_aid.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

    llm_config = {
        "functions": [
            {
                "name": "retrieve_content",
                "description": "retrieve content for code generation and question answering.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
                        }
                    },
                    "required": ["message"],
                },
            },
        ],
        "config_list": config_list,
        "timeout": 60,
        "cache_seed": 42,
    }

    for agent in [cto, pm, reviewer]:
        # update llm_config for assistant agents.
        agent.llm_config.update(llm_config)

    for agent in [boss, cto, pm, reviewer]:
        # register functions for all agents.
        agent.register_function(
            function_map={
                "retrieve_content": retrieve_content,
            }
        )

    groupchat = autogen.GroupChat(
        agents=[boss, cto, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="random",
        allow_repeat_speaker=False,
    )

    manager_llm_config = llm_config.copy()
    manager_llm_config.pop("functions")
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=manager_llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=PROBLEM+" Must retrieve content using function calling.",
    )

print("FUNCTION CALLING RAG CHAT")
function_calling_rag_chat()

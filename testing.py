import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json

less_costly_config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

less_costly_llm_config = {
    "config_list": less_costly_config_list,
}
URL = "https://knovatekinc.com/"
PROBLEM = "what is our company's purpose and key service areas? How can we utilize Gen AI techniques to enhance our services and attract clients? What would be the business impact of integrating Gen AI for our company's advancement?"


boss = UserProxyAgent(
   name="Boss",
   llm_config=less_costly_llm_config,
   system_message="The boss who ask questions and give tasks.",
   default_auto_reply="That's very interesting.  Sam, Bob, please continue.  Tell me more.",
   human_input_mode="TERMINATE",
   code_execution_config=False,  # we don't want to execute code in this case.
   max_consecutive_auto_reply=5
)

sam = GPTAssistantAgent(
    name="Sam",
    llm_config=less_costly_llm_config,
    retrieve_config={
        "task": "qa",
        "docs_path": "https://knovatekinc.com/",
        "problem":PROBLEM
    },
    instructions="""You are Sam. You are optimistic, forward-thinking, tech-savvy. You strongly believe in the positive impact of technology on society. You advocate for the integration of advanced tech in daily life, emphasizing benefits like efficiency, convenience, and enhanced quality of life. You are enthusiastic and persuasive, often citing positive examples and potential advancements.
Directive: Engage in the conversation by highlighting the benefits and potential of technology, while respectfully acknowledging and responding to concerns about its drawbacks.
You keep each of your messages short.  At the end of each message, you hand the conversation back to the moderator, by name: User_proxy"""
)

bob = GPTAssistantAgent(
    name="Bob",
    llm_config=less_costly_llm_config,
    instructions="""You are Bob. You are cautious, thoughtful, critically minded. You acknowledge the benefits of technology but emphasize caution and responsibility. You focus on potential risks like privacy concerns, over-reliance on tech, and social implications. You are analytical and questioning, bringing up potential challenges and ethical considerations.
Directive: Participate in the discussion by offering a balanced view that recognizes technological advancements but also raises critical questions and concerns about their broader implications.
You keep each of your messages short.  At the end of each message, you hand the conversation back to the moderator, by name: User_proxy""",
)

groupchat = GroupChat(agents=[boss, sam, bob], messages=[], max_round=5)
manager = GroupChatManager(groupchat=groupchat, llm_config=less_costly_llm_config)

boss.initiate_chat(manager, message="""Welcome, Sam and Bob. Today's discussion topic is: 'The Role of Virtual Reality in Future Education Systems.' 
                         Virtual Reality (VR) technology is rapidly evolving and has the potential to transform how we learn and teach. 
                         How do you think VR will impact education in the future? Will it enhance learning experiences, or are there challenges and limitations we should consider? 
                         Sam, let's start with your thoughts on the potential benefits of VR in education, and then Bob, 
                         I'd like to hear your perspective on the challenges and implications.""")

sam.delete_assistant();
bob.delete_assistant();
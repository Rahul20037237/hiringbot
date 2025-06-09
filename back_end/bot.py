from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import Graph, END
from langchain.schema import HumanMessage, AIMessage

from .templates import Templates
from .smith import LangSmithTracer

from .config import settings


def route_next_stage(state):
    print("Routing State Flags:", state)
    if not state.get("greeting_done", False):
        return "greeting"
    elif not state.get("info_done", False):
        return "info"
    elif not state.get("tech_done", False):
        return "tech_stack"
    elif state.get("hiring_question_count", 0) < 6:
        return "hiring"
    else:
        return END


def _build_prompt(template: str, history, input_str: str):
    return ChatPromptTemplate.from_messages([
        ('system', template),
        *[(msg.type, msg.content) for msg in history[-4:]],
        ('human', '{input}')
    ]), {"input": input_str}


class LangGraphHiringBot:
    def __init__(self):
        self.templates = Templates()
        self.llm = ChatGroq(
            api_key=settings.GROQ_API.get_secret_value(),
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=1024,
        )
        self.tracer = LangSmithTracer()
        self.conversations = {}

    def _run_stage(self, state, template, flag_name, next_stage):
        input_str = state.get("user_input", "")
        conversation_id = state.get("conversation_id", "default")
        history = self.conversations.setdefault(conversation_id, {
            "messages": [],
            "flags": {
                "greeting_done": False,
                "info_done": False,
                "tech_done": False,
                "hiring_done": False,
                "hiring_question_count": 0
            }
        })["messages"]

        self.tracer.start_trace(conversation_id, input_str, state.get("stage", "unknown"))

        prompt, inputs = _build_prompt(template, history, input_str)
        response = (prompt | self.llm | StrOutputParser()).invoke(inputs)

        history.extend([
            HumanMessage(content=input_str),
            AIMessage(content=response)
        ])

        new_state = {
            **state,
            "response": response,
            "stage": next_stage,
            flag_name: True
        }

        self.tracer.end_trace(conversation_id, response, new_state)

        return new_state

    def greeting_node(self, state):
        print('Running greeting_node')
        return self._run_stage(state, self.templates.greeting, "greeting_done", "info")

    def info_node(self, state):
        print('Running info_node')
        return self._run_stage(state, self.templates.info, "info_done", "tech_stack")

    def tech_stack_node(self, state):
        print('Running tech_stack_node')
        return self._run_stage(state, self.templates.tech_stack, "tech_done", "hiring")

    def hiring_node(self, state):
        print('Running hiring_node')
        count = state.get("hiring_question_count", 0) + 1
        updated_state = self._run_stage(state, self.templates.hiring_prompt, "hiring_done", "hiring")
        updated_state["hiring_question_count"] = count
        return updated_state


    def create_graph(self):
        graph = Graph()

        graph.add_node("greeting", self.greeting_node)
        graph.add_node("info", self.info_node)
        graph.add_node("tech_stack", self.tech_stack_node)
        graph.add_node("hiring", self.hiring_node)

        graph.add_conditional_edges("greeting", route_next_stage, {"info": "info", END: END})
        graph.add_conditional_edges("info", route_next_stage, {"tech_stack": "tech_stack", END: END})
        graph.add_conditional_edges("tech_stack", route_next_stage, {"hiring": "hiring", END: END})
        graph.add_conditional_edges("hiring", route_next_stage, {END: END})

        graph.set_entry_point("greeting")
        return graph.compile()

    def process_message(self, user_input: str, conversation_id: str = "default"):
        conv = self.conversations.setdefault(conversation_id, {
            "messages": [],
            "flags": {
                "greeting_done": False,
                "info_done": False,
                "tech_done": False,
                "hiring_done": False,
                "hiring_question_count": 0
            }
        })

        state = {
            "user_input": user_input,
            "conversation_id": conversation_id,
            **conv["flags"]
        }

        current_stage = route_next_stage(state)

        node_funcs = {
            "greeting": self.greeting_node,
            "info": self.info_node,
            "tech_stack": self.tech_stack_node,
            "hiring": self.hiring_node,
            END: lambda s: {"stage": END, "response": "Conversation complete."}
        }

        node_func = node_funcs.get(current_stage, node_funcs[END])
        result = node_func(state)

        for key in conv["flags"].keys():
            if key in result:
                conv["flags"][key] = result[key]

        return {
            "response": result.get("response", ""),
            "stage": result.get("stage", "complete")
        }


if __name__ == "__main__":
    print("\U0001F916 AI Hiring Bot - Simulated Chat\n")
    bot = LangGraphHiringBot()
    while True:
        user_input = input("\U0001F464 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nExiting bot. Goodbye!")
            break
        result = bot.process_message(user_input)
        print(f"\U0001F916 Bot ({result['stage']}): {result['response']}\n")

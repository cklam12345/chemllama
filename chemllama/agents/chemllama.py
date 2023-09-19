import langchain
import nest_asyncio
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, chains
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from rmrkl import ChatZeroShotAgent, RetryAgentExecutor

from .prompts import FORMAT_INSTRUCTIONS, QUESTION_PROMPT, REPHRASE_TEMPLATE, SUFFIX
from .tools import make_tools
from langchain.llms import CTransformers

def _make_llm(model, temp, verbose, api_key):
    if model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
        llm = LlamaCpp(
        model_path="openorca-platypus2-13b.gguf.q4_0.bin",
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        n_ctx=2048,
        verbose=True, # Verbose is required to pass to the callback manager,
        callbacks=[StreamingStdOutCallbackHandler()] if verbose else [None]
    )
    elif model.startswith("text-"):
        llm = LlamaCpp(
        model_path="openorca-platypus2-13b.gguf.q4_0.bin",
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        n_ctx=2048,
        verbose=True, # Verbose is required to pass to the callback manager,
        callbacks=[StreamingStdOutCallbackHandler()] if verbose else [None]
    )
    else:
        raise ValueError(f"Invalid model name: {model}")
    return llm


class ChemLlama:
    def __init__(
        self,
        tools=None,
        model="gpt-3.5-turbo-0613",
        tools_model="gpt-3.5-turbo-0613",
        temp=0.75,
        max_iterations=40,
        verbose=True,
        openai_api_key: str = None,
        api_keys: dict = None
    ):
        try:
            self.llm = _make_llm(model, temp, verbose, openai_api_key)
        except:
            return "Invalid openai key"

        if tools is None:
            tools_llm = _make_llm(tools_model, temp, verbose, openai_api_key)
            tools = make_tools(
                tools_llm,
                api_keys = api_keys,
                verbose=verbose
            )
        # Initialize agent
        self.agent_executor = RetryAgentExecutor.from_agent_and_tools(
            tools=tools,
            agent=ChatZeroShotAgent.from_llm_and_tools(
                self.llm,
                tools,
                suffix=SUFFIX,
                format_instructions=FORMAT_INSTRUCTIONS,
                question_prompt=QUESTION_PROMPT,
            ),
            verbose=True,
            max_iterations=max_iterations,
            #return_intermediate_steps=True,
        )

        rephrase = PromptTemplate(
            input_variables=["question", "agent_ans"], template=REPHRASE_TEMPLATE
        )

        self.rephrase_chain = chains.LLMChain(prompt=rephrase, llm=self.llm)

    #nest_asyncio.apply()  # Fix "this event loop is already running" error

    def run(self, prompt):
        outputs = self.agent_executor({"input": prompt})
        return outputs['output']
        # Parse long output (with intermediate steps)
        #intermed = outputs["intermediate_steps"]

        #final = ""
        #for step in intermed:
        #    final += f"Thought: {step[0].log}\n" f"Observation: {step[1]}\n"
        #final += f"Final Answer: {outputs['output']}"

        #rephrased = self.rephrase_chain.run(question=prompt, agent_ans=final)
        #print(f"ChemLlama output: {rephrased}")
        #return rephrased

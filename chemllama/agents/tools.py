import os

from langchain import agents
from langchain.base_language import BaseLanguageModel

from chemllama.tools import *


def make_tools(
        llm: BaseLanguageModel,
        api_keys: dict = {},
        verbose=True
):
    serp_key = os.getenv("SERP_API_KEY")
    rxn4chem_api_key = os.getenv("RXN4CHEM_API_KEY")

    all_tools = agents.load_tools([
        "python_repl",
        "ddg-search",
        "wikipedia",
        #"human"
    ])

    all_tools += [
        Query2SMILES(),
        Query2CAS(),
        PatentCheck(),
        MolSimilarity(),
        SMILES2Weight(),
        FuncGroups(),
        ExplosiveCheck(),
        SafetySummary(llm=llm),
        #LitSearch(llm=llm, verbose=verbose),
    ]
    if rxn4chem_api_key:
        all_tools.append(RXNPredict(rxn4chem_api_key))

    return all_tools

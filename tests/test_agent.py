import chemllama


def test_version():
    assert chemllama.__version__


def test_agent_init():
    chem_model = chemllama.ChemLlama(
        model="gpt-4-0613",
        temp=0.1,
        max_iterations=2,
        api_keys={}
    )
    chem_model.run("What is the molecular weight of tylenol?")

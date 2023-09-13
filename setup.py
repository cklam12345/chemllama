from setuptools import find_packages, setup

# for typing
__version__ = "0.0.0"
exec(open("chemllama/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chemllama",
    version=__version__,
    description="Accurate solution of reasoning-intensive biochemical tasks, poweredby LLMs.",
    author="Chin Keong Lam",
    author_email="cklam@patho.ai",
    url="https://www.patho.ai",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "ipython",
        "rdkit",
        "synspace",
        "molbloom",
        "paper-qa>=3.0.0",
        "google-search-results",
        "langchain",
        "nest_asyncio",
        "tiktoken",
        "rmrkl",
        "paper-scraper@git+https://github.com/blackadad/paper-scraper.git",
        "streamlit",
        "rxn4chemistry",
        "duckduckgo-search",
        "wikipedia"
    ],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

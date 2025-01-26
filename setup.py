# (optional, for packaging the project)

from setuptools import setup, find_packages

setup(
    name="chatbot-project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "requests",
        "langchain",
        "openai",
        "chromadb",
    ],
)

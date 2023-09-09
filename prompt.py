from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'

loader = ConfluenceLoader(
    url="https://igops.atlassian.net/wiki", username="igor.oliveira@e-core.com", api_key="ATATT3xFfGF0oS7L1Xy3aDxWqQp6rAXeww169zyqTVABPaeDzMzFoSX_KPgNgumTQ6QSaNVslDEIGi25vbgXgOKssxvcpmcXn2I_eNHQBIVfH57LAW6YhJkjQr35chyyvxussVHHwiRe9VWkS5VqQErtla9D1vdCzufZ8iLLPlRevKLGQ20GUcE=6B282381"
)
documents = loader.load(space_key="DKMA0001", include_attachments=False, limit=50)

text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
text_splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=10, encoding_name="cl100k_base")  # This the encoding for text-embedding-ada-002
texts = text_splitter.split_documents(texts)

embeddings = HuggingFaceEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embeddings)

question = "What is Migration Accelerator? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

retriever = vectordb.as_retriever() #Top4-Snippets
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",retriever=retriever)

print(qa.run(question))
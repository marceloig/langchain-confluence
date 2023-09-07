from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import ConfluenceLoader

import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'

question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

# prompt = PromptTemplate(template=template, input_variables=["question"])
# repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
# llm = HuggingFaceHub(
#     repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
# )
# llm_chain = LLMChain(prompt=prompt, llm=llm)

# print(llm_chain.run(question))

loader = ConfluenceLoader(
    url="https://igops.atlassian.net/wiki", username="igor.oliveira@e-core.com", api_key="ATATT3xFfGF0tU_woa3hEffedbku9aB2S3wtqHdAjRxYAlP4n_jSQg8nvYFqWgYKCiG9pFUjg-KCgVI2v5wrhf6xhEWpwWMw0WhWENkcZbm3swvQhT6xLrJCmVgfIsHh9uWDPE9AtSxg5pYDriehsYZuyeXsUcAaJMabYZPep-Pv1V8NMHFOwBU=41E7F0C6"
)
documents = loader.load(space_key="DKMA0001", include_attachments=False, limit=50)
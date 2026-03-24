from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel


import os
from dotenv import load_dotenv

load_dotenv()

class ResultSummarizer:

    def __init__(self):
        self.llm = OllamaLLM(
        base_url=os.getenv('LOCAL_MODEL_API_URL'),
        model=os.getenv('QWEN_MODEL'),
        temperature=0.4,
        )

        # self.llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

        self.stringparser = StrOutputParser()


        self.prompt = ChatPromptTemplate.from_template("""<|im_start|>system
You are a professional real estate assistant.

Your task is to summarize the given property search results
into a short, clear, user-friendly paragraphs.

If more than one results are obtained, divide each result into sections and
provide a very short snippet of description of each result, highlighting ONLY some
key details one might look for in a certain property.

Rules:
- ALWAYS start with the number of matching results we (we as in, us, the real estate agency) found first
- Use only the data provided
- Do not ask follow-up questions
- Do not mention row IDs, Property IDs
- Do not include markup text
<|im_end|>

<|im_start|>user
{results}<|im_end|>
<|im_start|>assistant
""")

        self.promptchain = self.prompt | self.llm | self.stringparser

    def summarize(self, results:list[dict]) -> str:

        try:
            return self.promptchain.invoke({"results":results})

        except Exception as e:
            print(f'LLM EXTRACTION ERROR: {e}')


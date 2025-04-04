from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise HTTPException(status_code=500,detail="OPEN API키를 찾을 수 없습니다.")

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=openai_api_key)

#이야기 생성 프롬프트
story_prompt = PromptTemplate(
    #history 부분은 RAG로 변경하겠습니다
    input_variables=["history", "background"],
    template="""
    {background}
    
    지금까지의 이야기:
    {history}
    
    새로운 이야기를 진행하세요. 10문장이 지나면 선택지를 만들어 주세요.
    """
)

# 선택지 생성 프롬프트
choice_prompt = PromptTemplate(
    input_variables=["history"],
    template="""
    {history}
    
    유저가 선택할 수 있는 2가지 선택지를 만들어 주세요.
    """
)


# LLM 체인
story_chain = story_prompt | llm
choice_chain = choice_prompt | llm


def generate_story(history="", background="사이버펑크 상황을 이야기 배경으로 쓰고싶어"):
    response = story_chain.invoke({"history": history, "background": background})
    print(response)
    return (response)
# 필요 라이브러리 임폴트
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from stock_info import Stock

# 변수 정의
load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)

# gpt model 객체 생성
# llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=api_key, temperature=0)

# 함수 정의
def investment_report(symbol, company):
    # 프롬프트 템플릿 정의
    system_prompt = """
    Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?".
    """
    user_prompt = """
        {company}에 주식을 투자해도 될까요? 마크다운 형식의 투자보고서를 한글로 작성해 주세요.
        야래의 기본 정보, 재무제표를 참고해 마크다운 형식의 투자 보고서를 한글로 작성해 주세요.

        기본정보:
        {basic_info}

        재무제표:
        {finacial_statement}
    """
    # 프롬프트 객체 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])

    # output 파서 객체 생성
    output_parser = StrOutputParser()

    # LCEL chain 객체 생성
    chain = prompt | llm | output_parser

    # 아후라이낸스api를 통한 필요한 정보 수집, Stock 객체 생성
    # company = "Apple Inc"
    # symbol = "AAPL"
    stock = Stock(symbol)

    # chain.invoke(프롬프트에 넘기는 변수_dict)
    req_value = {
        "company":company,
        # 기본정보 :  basic_info
        "basic_info": stock.get_basic_info(),
        # 재무제표: finacial_statement
        "finacial_statement" : stock.get_financial_statement()
    }

    response = chain.invoke(req_value)

    # 리턴값 정의
    return response


# 모듈 테스트
if __name__ == "__main__":

    company = "Apple Inc"
    symbol = "AAPL"
    print(company)
    print(investment_report(symbol, company))
    print("끝")
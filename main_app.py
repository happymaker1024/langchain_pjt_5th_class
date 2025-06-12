import streamlit as st
from report_service import investment_report
from stock_info import Stock
from search_index import search_company, SearchResult

st.title("AI 투자 보고서 생성 서비스")
search_symbol = st.text_input("회사 심볼", "AAPL")
# company_list = ["AAPL: Apple Inc",
#                 "APLE: Apple Hospitality REIT Inc"]

company_info = search_company(search_symbol)
hits = company_info['hits']

company_list = [SearchResult(hit) for hit in hits]
company_selected = st.selectbox("회사명 선택", company_list, index=0)
print(company_selected)
# 회사 이름
# search_symbol = "MSFT" 
# company_selected = "MicroSoft"
# 선택한 회사의 심볼
search_symbol = company_selected.symbol
# 선택한 회사의 회사명
company_selected = company_selected.name
  

print(search_symbol)
print(company_selected)

tabs = ["주식 정보", "투자 보고서"]
tab1, tab2 = st.tabs(tabs)

# 주식 거래량 차트로 시각화
with tab1:  
    st.header(f"{company_selected}의 6개월 주식 거래량")
    stock = Stock(search_symbol)
    volume = stock.get_stock_volume()
    st.line_chart(volume, use_container_width=True)


# LLM이 만든 투자 보고서 출력
with tab2:
    # AI 투자 보고서 출력

    st.header(f"{company_selected} AI 투자보고서")

    if st.button("투자 보고서 생성"):
        with st.spinner(text="투자 보고서 생성 중..."):
            report = investment_report(search_symbol, company_selected)
            st.success("투자 보고서 생성 완료!")            
        st.write(report)
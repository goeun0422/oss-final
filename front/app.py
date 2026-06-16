import streamlit as st
import requests

st.set_page_config(page_title="광운대 공강 생존기", page_icon="🍚")

st.title("🍚 광운대 공강 생존 식당 추천 시스템")
st.write("시간, 지갑 사정, 그리고 내 배고픔에 딱 맞는 식당을 찾아드립니다.")

with st.form("meal_form"):
    st.subheader("현재 상황을 입력해주세요")
    
    location_input = st.radio("현재 가장 가까운 건물은?", ["80주년기념관 (정문 쪽)", "새빛관 (후문 쪽)"], horizontal=True)
    budget = st.number_input("현재 지갑 사정 (원)", min_value=0, step=1000, value=8000)
    time_left = st.slider("다음 수업까지 남은 시간 (분)", 10, 120, 50)
    
    # 배고픔 게이지(1~5)
    hunger_text = st.radio(
        "현재 배고픔 게이지", 
        ["🍚", "🍚🍚", "🍚🍚🍚", "🍚🍚🍚🍚", "🍚🍚🍚🍚🍚"], 
        horizontal=True,
        index=2 # 기본값 3점
    )
    
    submitted = st.form_submit_button("🔥 최적의 식당 찾기")

if submitted:
    loc_data = "기념관" if "기념관" in location_input else "새빛관"
    
    hunger_data = len(hunger_text)
    
    payload = {
        "location": loc_data,
        "budget": budget,
        "time_left": time_left,
        "hunger": hunger_data
    }
    
    api_url = "http://backend:8000/recommend"
    
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            results = response.json()
            
            st.balloons()
            
            st.markdown("---")
            st.success("✨ 분석 완료! 당신을 위한 추천 식당 TOP 3입니다.")
            
            for i, res in enumerate(results):
                if i == 0:
                    st.subheader(f"🥇 1위: {res['name']}")
                    st.info(f"💸 예상 가격: {res['price']}원 | ⏱️ 예상 소요 시간: {res.get('time', '?')}분")
                else:
                    st.write(f"**{i+1}위:** {res['name']} ({res['price']}원)")
                
                st.caption(f"💡 {res['reason']}")
                
                if res['price'] > 0:
                    map_link = f"https://map.kakao.com/link/search/광운대 {res['name']}"
                    st.markdown(f"[🗺️ 지도에서 **{res['name']}** 위치 보기]({map_link})")
                st.write("") 
                
        else:
            st.error("서버에서 올바른 응답을 받지 못했습니다.")
    except Exception as e:
        st.error(f"백엔드 연결 오류가 발생했습니다. Docker 상태를 확인하세요! (에러: {e})")
import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="광운대 공강 생존 식당 추천", page_icon="🍚", layout="wide")

st.title("🍚 광운대 공강 생존 식당 추천")
st.write("시간, 예산, 배고픔 정도를 고려하여 지금 가장 적합한 식당을 추천해드립니다.")

with st.sidebar:
    st.header("현재 상황 입력")
    with st.form("meal_form"):
        location_input = st.radio("현재 가장 가까운 건물은?", ["80주년기념관 (정문 쪽)", "새빛관 (후문 쪽)"])
        budget = st.number_input("현재 지갑 사정 (원)", min_value=0, step=1000, value=8000)
        time_left = st.slider("다음 수업까지 남은 시간 (분)", 10, 120, 50)
        
        hunger_text = st.radio(
            "현재 배고픔 게이지", 
            ["🍚", "🍚🍚", "🍚🍚🍚", "🍚🍚🍚🍚", "🍚🍚🍚🍚🍚"], 
            index=2
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
            
            # 예외 처리: 조건에 맞는 식당이 없을 때
            if results[0]["name"] == "추천 불가":
                st.warning(f"🚨 {results[0]['reason']}")
                
            # 조건에 맞는 식당이 있을 때 
            else:
                st.toast("🍚 최적의 식당을 찾았습니다!")
                
                st.markdown("""
                <div style="
                padding:15px;
                background:#F6EDEE;
                border-left:6px solid #7A0019;
                border-radius:10px;
                font-size:20px;
                font-weight:bold;
                margin-bottom:20px;
                ">
                🍚 추천 결과 TOP 3
                </div>
                """, unsafe_allow_html=True)
                
                medals = ["🥇", "🥈", "🥉"]
                
                for i, res in enumerate(results):
                    with st.container(border=True):
                        st.subheader(f"{medals[i]} {res['name']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("가격", f"{res['price']}원")
                        with col2:
                            st.metric("시간", f"{res['time']}분")
                        
                        st.caption(f"💡 {res['reason']}")
                        
                        if res['price'] > 0:
                            query = urllib.parse.quote(f"광운대 {res['name']}")
                            map_link = f"https://map.kakao.com/link/search/{query}"
                            st.link_button("🗺️ 지도 보기", map_link)
                
        else:
            st.error("서버에서 올바른 응답을 받지 못했습니다.")
    except Exception as e:
        st.error(f"백엔드 연결 오류가 발생했습니다. Docker 상태를 확인하세요! (에러: {e})")
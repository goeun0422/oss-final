from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MealRequest(BaseModel):
    location: str
    budget: int
    time_left: int
    hunger: int

# 광운대 맞춤형 식당 데이터베이스
RESTAURANTS = [
    {"name": "후문식당", "location": "새빛관", "price": 8000, "time": 45, "hungry": 5},
    {"name": "로스2000", "location": "새빛관", "price": 12000, "time": 70, "hungry": 5},
    {"name": "카츠백", "location": "새빛관", "price": 12000, "time": 50, "hungry": 5},
    {"name": "김가네", "location": "새빛관", "price": 7000, "time": 35, "hungry": 3},
    {"name": "서초우동", "location": "새빛관", "price": 6000, "time": 40, "hungry": 3},
    {"name": "뉴욕쟁이디저트", "location": "새빛관", "price": 5000, "time": 20, "hungry": 2},
    {"name": "카페니니", "location": "새빛관", "price": 5000, "time": 20, "hungry": 2},
    {"name": "메가MGC커피", "location": "새빛관", "price": 2500, "time": 15, "hungry": 1},
    {"name": "도미노피자", "location": "새빛관", "price": 20000, "time": 55, "hungry": 5},
    {"name": "컴포즈커피", "location": "새빛관", "price": 1500, "time": 10, "hungry": 1},
    
    {"name": "윤스쿡", "location": "기념관", "price": 11000, "time": 50, "hungry": 5},
    {"name": "이층집", "location": "기념관", "price": 8000, "time": 45, "hungry": 4},
    {"name": "미미식당", "location": "기념관", "price": 7500, "time": 45, "hungry": 4},
    {"name": "마루덮밥", "location": "기념관", "price": 7500, "time": 40, "hungry": 3},
    {"name": "푸른스시", "location": "기념관", "price": 14000, "time": 50, "hungry": 5},
    {"name": "고씨네", "location": "기념관", "price": 8500, "time": 40, "hungry": 4},
    {"name": "민들레국시", "location": "기념관", "price": 6500, "time": 35, "hungry": 3},
    {"name": "카페 베르데", "location": "기념관", "price": 5000, "time": 15, "hungry": 2},
    {"name": "이디야", "location": "기념관", "price": 3200, "time": 15, "hungry": 1},
    {"name": "빽다방", "location": "기념관", "price": 1500, "time": 10, "hungry": 1},
    {"name": "세븐일레븐", "location": "기념관", "price": 4000, "time": 10, "hungry": 2}
]

@app.post("/recommend")
def get_recommendation(data: MealRequest):
    candidates = []
    
    for r in RESTAURANTS:
        # 1. 예산 및 시간 필터링 (조건 안 맞으면 탈락)
        if r["price"] > data.budget:
            continue
            
        travel_time = 0 if r["location"] == data.location else 10
        total_time_required = r["time"] + travel_time
        
        if total_time_required > data.time_left:
            continue
            
        # 2. 정교한 점수 계산
        score = 0
        score += 10 - (abs(r["hungry"] - data.hunger) * 2) # 배고픔 일치도
        
        if r["location"] == data.location:
            score += 10 # 가까운 위치 가산점
            
        if data.budget - r["price"] >= 3000:
            score += 5 # 예산 여유 가산점
            
        # 3. 상황에 맞는 동적 추천 이유 생성
        reasons = []
        if r["location"] == data.location:
            reasons.append("현재 위치와 가까워요")
        if r["price"] <= data.budget:
            reasons.append("예산 안에서 해결 가능해요")
        if total_time_required <= data.time_left:
            reasons.append("공강 시간 안에 충분히 이용 가능해요")
            
        diff = abs(r["hungry"] - data.hunger)
        if diff == 0:
            reasons.append("현재 배고픔에 딱 맞는 메뉴예요")
        elif diff == 1:
            reasons.append("배고픔 정도와 잘 맞아요")
            
        reason_text = ", ".join(reasons)
        
        candidates.append({
            "name": r["name"],
            "price": r["price"],
            "time": total_time_required,
            "score": score,
            "reason": reason_text
        })
        
    # 점수 높은 순으로 정렬하여 3개 추출
    candidates.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)
    top_3 = candidates[:3]
    
    # 예외 처리
    if not top_3:
        return [{
            "name": f"{data.location} 근처 편의점 런", 
            "price": 0, 
            "reason": "현재 잔고와 남은 시간으로는 갈 수 있는 식당이 없습니다!"
        }]
        
    return top_3
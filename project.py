# 컨트롤 + 쉬프트 + p -> python:selct interpreter // 환경 선택후 터미널 재실행
# 폴더 이동후 패키지 설치
# pip install fastapi uvicorn python-dotenv httpx // pip 설치 해주어야함 
# FastAPI 쓸때 서버 실행 명령어 
    # uvicorn project:app --reload --port 8000  // FastAPI 쓸때 서버 실행 명령어 
        # uvicorn (파일명).py:app --reload --port 8000 // () 괄호안에꺼 적어주는거임 
# pip install google-generativeai

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import dotenv
import httpx
import google.generativeai as genai

dotenv.load_dotenv()

app = FastAPI()

# CORS 설정
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
GOOGLE_API_URL = "https://generativeai.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
model = genai.GenerativeModel('gemini-1.5-flash')

genai.configure(api_key=API_KEY)
# --- Pydantic 모델 정의 ---

class HistoryItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: List[HistoryItem]

class MenuItem(BaseModel):
    food_name: str
    price: int

class Store(BaseModel):
    id: int
    name: str
    address: str
    contact: str
    representative_food: str
    representative_food_price: int
    business_hours: str
    closed_day: str
    image: str
    menu: List[MenuItem]

class GoodStoreRequest(BaseModel):
    address: str

# --- 샘플 데이터 ---

stores = [
    Store(
        id=1,
        name="가게 A",
        address="서울 강남구",
        contact="010-1234-5678",
        representative_food="김밥",
        representative_food_price=3000,
        business_hours="10:00 - 22:00",
        closed_day="매주 일요일",
        image="https://via.placeholder.com/300",
        menu=[
            MenuItem(food_name="김밥", price=3000),
            MenuItem(food_name="떡볶이", price=5000),
        ],
    ),
    Store(
        id=2,
        name="가게 B",
        address="서울 종로구",
        contact="010-9876-5432",
        representative_food="라면",
        representative_food_price=3500,
        business_hours="11:00 - 23:00",
        closed_day="매주 월요일",
        image="https://via.placeholder.com/300",
        menu=[
            MenuItem(food_name="라면", price=3500),
            MenuItem(food_name="치킨", price=8000),
        ],
    ),
]

# --- API 엔드포인트 ---

@app.get("/")
async def root():
    return {"message": "api 호출 성공"}
import traceback

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        history = request.history
        formatted_history = [
            {"role": item.role, "parts": [{"text": item.content}]} for item in history
        ]

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        json_data = {
            "contents": formatted_history
        }

        print("📤 요청 데이터:", json_data)
        try:
            result = model.generate_content(formatted_history)
        except Exception as e:
            print("사용량에 초과하였습니다.")
            return JSONResponse(status_code=429, content=f"gemini api 사용량이 초과하였습니다: {str(e)}")
        print(result)
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(GOOGLE_API_URL, json=json_data, headers=headers)
        #     response.raise_for_status()
        #     result = response.json()

        # print("📥 응답 데이터:", result)

        # 응답 구조에 맞게 파싱
        # response_text = result["candidates"][0]["content"]["parts"][0]["text"]
        response_text = result.text
        updated_history = [*history, {"role": "model", "content": response_text}]

        return {"message": "텍스트 생성 성공", "history": updated_history}

    except Exception as e:
        print("❌ 예외 발생:", str(e))
        traceback.print_exc()
        raise JSONResponse(status_code=500, content=f"텍스트 생성에 실패하였습니다: {str(e)}")

@app.post("/api/good-store")
async def good_store(request: GoodStoreRequest):
    address = request.address
    if not address:
        raise JSONResponse(status_code=400, content="주소를 제공해 주세요.")

    filtered_stores = [store for store in stores if address in store.address]

    if filtered_stores:
        return {"success": True, "stores": filtered_stores}
    else:
        return {"success": False, "message": "해당하는 착한 가게가 없습니다."}
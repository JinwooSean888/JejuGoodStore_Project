# pip install fastapi uvicorn python-multipart

import numpy as np 
import uvicorn, os, cv2
import pandas as pd
import tensorflow as tf

from typing import List
from fastapi import FastAPI, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

data = []
#df = pd.read_xml("https://www.seogwipo.go.kr/openapi/goodPriceService/", xpath=".//item")
engine = create_engine("mysql+pymysql://root:test@localhost:3307/auth")
df.to_sql(name="shops", con=engine, if_exists="replace", index=False)

df = pd.read_csv("C:/Mini_Project/제주시 착한가게 현황.csv", encoding="cp949")
print(df)

print("데이터 저장 완료!")

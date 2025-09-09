# pip install fastapi uvicorn python-multipart

import numpy as np 
import uvicorn, os, cv2
from typing import List
from fastapi import FastAPI, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import tensorflow as tf
import pandas as pd


data = []
df = pd.read_xml("https://www.seogwipo.go.kr/openapi/goodPriceService/", xpath=".//item")
engine = create_engine("mysql+pymysql://root:test@localhost:3307/auth")
df.to_sql(name="shops", con=engine, if_exists="replace", index=False)
print(df)

engine = create_engine("mysql+pymysql://root:비밀번호@localhost:3306/testdb", encoding="utf-8")

df.to_sql(name="shops", con=engine, if_exists="replace", index=False)
print("데이터 저장 완료!")

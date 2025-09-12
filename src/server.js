import express from "express";
import { dbPool } from "./dbConfig.js";
import { genAI } from "./geminiClient.js";
import cors from "cors";

const app = express();
app.use(express.json());

app.use(
  cors({ origin: ["http://localhost:3000", "http://192.168.0.51:3000"] })
);
// DB → Gemini → 응답
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.post("/ask", async (req, res) => {
  try {
    const { question, filters } = req.body;
    const { indutyType, emdType } = filters || {};
    console.log(indutyType);
    // DB 조회 (프리페어드 스테이트먼트 사용)
    const [rows] = await dbPool.query(
      `SELECT * 
       FROM auth.shops 
       WHERE indutyType = ? 
         AND emdType = ? 
         AND prdlstCn LIKE ?;`,
      [indutyType, emdType, `%${question}%`] // ✅ LIKE 검색 안전하게 처리
    );
    const shopList = rows
      .map((r) => `${r.bsshNm} (메뉴: ${r.prdlstCn})`)
      .join("\n");
    // console.log("DB에서 불러온 가게 리스트:", shopList);
    // Gemini 호출
    const prompt = `
    사용자가 질문: "${question}"
    다음은 DB에서 불러온 가게 리스트입니다:
    ${shopList}

    위 리스트를 기반으로 질문에 맞게 대답해주세요.
    `;

    console.log(prompt);
    const result = await model.generateContent(prompt);
    const answer = result.response.text();

    return res.status(200).json({ answer, rows });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "서버 에러" });
  }
});

app.listen(8000, () => {
  console.log("🚀 Server running on http://localhost:8000");
});

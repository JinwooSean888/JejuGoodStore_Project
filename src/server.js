import express from "express";
import { dbPool } from "./dbConfig.js";
import { genAI } from "./geminiClient.js";

const app = express();
app.use(express.json());

// DB → Gemini → 응답
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.post("/ask", async (req, res) => {
  try {
    const { question, filters } = req.body;
    const { indutyType, emdType, prdlstCn } = filters || {};

    // 예시: DB에서 가게명 전부 불러오기
    const [rows] = await dbPool.query(
      "SELECT bsshNm, bsshTelno, prdlstCn FROM shops where indutyType = ? and emdNm = ?;",
      [indutyType, emdType] // 값은 배열로 전달
    );
    const shopList = rows
      .map((r) => `${r.bsshNm} (메뉴: ${r.prdlstCn})`)
      .join("\n");
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

    return res.status(200).json({ answer });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "서버 에러" });
  }
});

app.listen(3000, () => {
  console.log("🚀 Server running on http://localhost:3000");
});

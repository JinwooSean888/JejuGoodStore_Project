const express = require("express");
const app = express();
app.use(express.json());
app.get("/", async (req, res) => {
  res.status(200).json({ message: "api 호출 성공" });
});

app.post("/chat", async (req, res) => {
  try {
    const { history } = req.body;
    console.log(history);
  } catch (e) {
    console.log(e);
    res.status(500).json({ message: "텍스트 생성에 실패하였습니다." });
  }
});

app.listen(8000, () => {
  console.log("서버 실행중");
});

import mysql from "mysql2/promise";
import dotenv from "dotenv";
dotenv.config();

export const dbPool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  port: parseInt(process.env.DB_PORT) || 3307,
});

console.log("Host", process.env.DB_HOST, parseInt(process.env.DB_PORT));

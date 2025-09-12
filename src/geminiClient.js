import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
dotenv.config();

export const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
export const genAI1 = new GoogleGenerativeAI(process.env.GEMINI_API_KEY1);
export const genAI2 = new GoogleGenerativeAI(process.env.GEMINI_API_KEY2);

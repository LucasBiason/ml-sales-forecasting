import axios from "axios";
import type { PropertyInput, PredictionResponse, HealthResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const healthCheck = async (): Promise<HealthResponse> => {
  const response = await api.get<HealthResponse>("/health");
  return response.data;
};

export const predictPrice = async (
  data: PropertyInput
): Promise<PredictionResponse> => {
  const response = await api.post<PredictionResponse>("/api/v1/predict", data);
  return response.data;
};

export default api;


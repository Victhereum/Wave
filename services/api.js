import axios from "axios";
import { BASE_URL } from "./resources";

// without bearer token
export const noAuthApi = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
  },
});

// with bearer token
export const authApi = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Accept": "application/json",
    "Content-Type": "multipart/form-data",
    "Authorization": "Bearer token here",
  },
});

// REST countries
export const countriesApi = axios.create({
  baseURL: "https://restcountries.com/v3.1/all?fields=flags,idd",
  timeout: 10000,
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
  },
});

import axios from "axios";
import { ERROR_MESSAGES } from "./exceptions";
import { toast } from "sonner";

export const s3BrowserAPIBaseV1 = axios.create({
  baseURL: `${import.meta.env.VITE_S3_BROWSER_URL}/api/v1/`,
  timeout: 5000,
  withCredentials: true,
})

s3BrowserAPIBaseV1.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const status = error.response?.status
    const uniqueCode = error.response?.data?.unique_code

    if (status === 401 && uniqueCode === "AUTHENTICATION_ERROR") {
      window.location.replace("/auth/login")
    }

    if (uniqueCode && uniqueCode in ERROR_MESSAGES) {
      const message =
        ERROR_MESSAGES[uniqueCode as keyof typeof ERROR_MESSAGES]

      toast.error(message, { position: "top-center" })
    } else {
      toast.error(`Неизвестная ошибка: ${uniqueCode}`, {
        position: "top-center",
      })
    }

    return Promise.reject(error)
  }
)
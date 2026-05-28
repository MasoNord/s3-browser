import axios from "axios"
import { toast } from "sonner"

import {
  ERROR_MESSAGES,
  type ErrorCode,
} from "./exceptions"

export const s3BrowserAPIBaseV1 = axios.create({
  baseURL: `${import.meta.env.VITE_S3_BROWSER_URL}/api/v1/`,
  timeout: 10000,
  withCredentials: true,
})

s3BrowserAPIBaseV1.interceptors.response.use(
  (response) => response,

  (error) => {

    if (!error.response) {

      if (error.code === "ECONNABORTED") {
        toast.error(
          ERROR_MESSAGES.TIMEOUT_ERROR,
          {
            position: "top-center",
          }
        )

      } else {
        toast.error(
          ERROR_MESSAGES.NETWORK_ERROR,
          {
            position: "top-center",
          }
        )
      }

      return Promise.reject(error)
    }

    const status: number | undefined =
      error.response?.status

    const uniqueCode: ErrorCode | undefined =
      error.response?.data?.unique_code

    if (
      status === 401 &&
      uniqueCode === "AUTHENTICATION_ERROR"
    ) {
      window.location.replace("/auth/login")

      return Promise.reject(error)
    }

    if (
      uniqueCode &&
      uniqueCode in ERROR_MESSAGES
    ) {

      toast.error(
        ERROR_MESSAGES[uniqueCode],
        {
          position: "top-center",
        }
      )

    } else {

      toast.error(
        ERROR_MESSAGES.UNHANDLED_EXCEPTION,
        {
          description:
            uniqueCode ??
            `HTTP ${status}`,

          position: "top-center",
        }
      )
    }

    return Promise.reject(error)
  }
)
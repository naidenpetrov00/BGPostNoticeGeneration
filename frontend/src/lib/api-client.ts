import Axios, { type InternalAxiosRequestConfig } from "axios";

import { env } from "../config/env";

function authRequestInterceptor(config: InternalAxiosRequestConfig) {
  if (config.headers) {
    config.headers.Accept = "application/json";
  }

  return config;
}

export const api = Axios.create({
  baseURL: env.API_URL,
});

api.interceptors.request.use(authRequestInterceptor);
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // if (error.response?.status === 401) {
    //   const searchParams = new URLSearchParams();
    //   const redirectTo =
    //     searchParams.get("redirectTo") || window.location.pathname;
    //   window.location.href = paths.auth.login.getHref(redirectTo);
    // }

    return Promise.reject(error);
  }
);

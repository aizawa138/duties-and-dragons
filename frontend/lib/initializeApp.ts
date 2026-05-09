import backendUrl from "@/lib/backendUrl";
import getCookie from "@/lib/getCookie";

type CsrfResponse = {
  csrfToken?: string;
};

export const initializeApp = async () => {
  const response = await fetch(backendUrl("/api/set-csrf/"), {
    method: "GET",
    credentials: "include", // CRITICAL: This allows the browser to save the cookie
  });

  if (!response.ok) {
    return getCookie("csrftoken") ?? "";
  }

  const data = (await response.json().catch(() => ({}))) as CsrfResponse;
  return data.csrfToken ?? getCookie("csrftoken") ?? "";
};

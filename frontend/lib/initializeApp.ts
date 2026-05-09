import backendUrl from "@/lib/backendUrl";

export const initializeApp = async () => {
  await fetch(backendUrl("/api/set-csrf/"), {
    method: "GET",
    credentials: "include", // CRITICAL: This allows the browser to save the cookie
  });
};

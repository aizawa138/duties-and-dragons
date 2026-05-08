export const initializeApp = async () => {
  await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL!}/api/set-csrf/`, {
    method: "GET",
    credentials: "include", // CRITICAL: This allows the browser to save the cookie
  });
};

"use client";

import LoginModal from "@/src/features/login/LoginModal";
import Logo from "../logo/Logo";
import { Button } from "@/src/components/ui/button/button";
import backendUrl from "@/lib/backendUrl";
import { initializeApp } from "@/lib/initializeApp";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

type AuthUser = {
  username: string;
  has_class: boolean;
};

async function fetchAuthUser(): Promise<AuthUser | null> {
  const response = await fetch(backendUrl("/api/get_user_info/"), {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json();
  return {
    username: data.username,
    has_class: data.has_class,
  };
}

export default function Header() {
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const router = useRouter();

  const refreshAuth = useCallback(async () => {
    try {
      setAuthUser(await fetchAuthUser());
    } catch {
      setAuthUser(null);
    } finally {
      setIsCheckingAuth(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    void fetchAuthUser()
      .then((user) => {
        if (isMounted) {
          setAuthUser(user);
        }
      })
      .catch(() => {
        if (isMounted) {
          setAuthUser(null);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsCheckingAuth(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleLogout = async () => {
    setIsLoggingOut(true);

    try {
      const csrfToken = await initializeApp();
      const response = await fetch(backendUrl("/api/logout/"), {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      });

      if (!response.ok) {
        console.error("Logout failed", response.status);
      }
    } finally {
      setAuthUser(null);
      setIsLoggingOut(false);
      router.push("/");
      router.refresh();
    }
  };

  return (
    <header className="sticky top-0 z-50 flex justify-end items-center p-4 bg-state-900 text-white bg-primary h-16">
      <div className="flex-1"></div>
      <div className="flex-1 text-center font-bold">
        <Logo />
      </div>
      <div className="flex flex-1 items-center justify-end gap-2">
        {!isCheckingAuth &&
          (authUser ? (
            <Button
              variant="secondary"
              size="default"
              onClick={handleLogout}
              disabled={isLoggingOut}
            >
              {isLoggingOut ? "Logging out..." : "Logout"}
            </Button>
          ) : (
            <>
              <LoginModal
                authenticationType="Login"
                variant="default"
                onAuthenticated={refreshAuth}
              />
              <LoginModal
                authenticationType="Signup"
                variant="secondary"
                onAuthenticated={refreshAuth}
              />
            </>
          ))}
      </div>
    </header>
  );
}

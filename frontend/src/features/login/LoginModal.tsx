"use client";

import * as Dialog from "@radix-ui/react-dialog";
import { Button } from "@/src/components/ui/button/button";
import { crossaintOne } from "@/public/fonts";
import { useState } from "react";
import { initializeApp } from "@/lib/initializeApp";
import { useRouter } from "next/navigation";
import backendUrl from "@/lib/backendUrl";

type AuthenticationType = {
  authenticationType: string;
  variant: "default" | "secondary";
  onAuthenticated?: () => void | Promise<void>;
};

export default function AuthenticationModal({
  authenticationType,
  variant,
  onAuthenticated,
}: AuthenticationType) {
  const [error, setError] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleClick = async () => {
    const csrfToken = await initializeApp();

    if (authenticationType === "Login") {
      try {
        setError("");
        const response = await fetch(backendUrl("/api/login/"), {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
          const { error } = await response.json();
          throw new Error(error);
        }

        const { username: registeredUsername, has_class: hasClass } =
          await response.json();
        await onAuthenticated?.();
        if (hasClass) {
          router.push(`/dashboard/${registeredUsername}`);
        } else {
          router.push(`/create/${registeredUsername}`);
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        setError(message);
      }
    } else if (authenticationType === "Signup") {
      try {
        const response = await fetch(backendUrl("/api/register/"), {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
          const { error } = await response.json();
          throw new Error(error);
        }

        const { username: registeredUsername, has_class: hasClass } =
          await response.json();

        await onAuthenticated?.();
        if (hasClass) {
          router.push(`/dashboard/${registeredUsername}`);
        } else {
          router.push(`/create/${registeredUsername}`);
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        setError(message);
      }
    }
  };

  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <Button variant={variant} size="default">
          {authenticationType}
        </Button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed backdrop-blur-xs inset-0" />
        <Dialog.Content className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10 bg-white rounded-2xl py-8 px-4 w-[90vw] max-w-md max-h-[90vh] overflow-y-auto border border-gray-500 sm:w-[70vw] lg:w-[40vw]">
          <Dialog.Title
            className={`${variant === "default" ? "text-primary" : "text-secondary"} text-3xl text-center font-semibold mb-4 ${crossaintOne.className}`}
          >
            {authenticationType}
          </Dialog.Title>
          <Dialog.Description className="mb-2 text-center text-gray-600">
            Duties & Dragons is a free to start task management + gaming
            application!
          </Dialog.Description>
          {error ? (
            <p className="bg-red-400 rounded-xl py-1 px-4">{error}</p>
          ) : (
            ""
          )}
          <div className="flex flex-col">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              className="border rounded-2xl border-gray-500 px-4 py-1 focus:outline-accent mb-4"
              placeholder="Username"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <label htmlFor="password">Password</label>
            <input
              type="password"
              className="border border-gray-500 rounded-2xl px-4 py-1 focus:outline-accent mb-6"
              placeholder="Password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button variant={variant} size="default" onClick={handleClick}>
              {authenticationType}
            </Button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

"use client";

import React, { useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { Button } from "@/src/components/ui/button/button";
import { crossaintOne } from "@/public/fonts";
import backendUrl from "@/lib/backendUrl";
import { initializeApp } from "@/lib/initializeApp";

interface ListItem {
  id: number;
  text: string;
  strength: number;
  intelligence: number;
  charisma: number;
  completed: boolean;
  deadline?: string;
}

interface TabsProps {
  tasks: ListItem[];
  setTasks: React.Dispatch<React.SetStateAction<ListItem[]>>;
  habits: ListItem[];
  setHabits: React.Dispatch<React.SetStateAction<ListItem[]>>;
}

export default function Tabs({
  tasks,
  setTasks,
  habits,
  setHabits,
}: TabsProps) {
  const [activeTab, setActiveTab] = useState<"tasks" | "habit">("tasks");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newItemText, setNewItemText] = useState("");
  const [newItemDeadline, setNewItemDeadline] = useState("");

  const today = new Date().toISOString().split("T")[0];

  const handleAIIntegration = async (
    endpoint: string,
    payload: { description: string; deadline?: string },
  ) => {
    const csrfToken = await initializeApp();
    const response = await fetch(backendUrl(endpoint), {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error ?? `Request failed with ${response.status}`);
    }

    const stats = data.stats ?? {};

    return {
      id: data.duty_id ?? data.habit_id ?? Date.now(),
      strength: Number(stats.strength ?? 0),
      intelligence: Number(stats.intelligence ?? 0),
      charisma: Number(stats.charisma ?? 0),
    };
  };

  const handleAdd = async () => {
    if (!newItemText.trim()) return;

    const newItem: ListItem = {
      id: Date.now(),
      text: newItemText,
      strength: 0,
      intelligence: 0,
      charisma: 0,
      completed: false,
      deadline: newItemDeadline || undefined,
    };

    try {
      if (activeTab === "tasks") {
        const createdItem = await handleAIIntegration("/api/create_duty/", {
          description: newItemText,
          deadline: newItemDeadline,
        });
        setTasks((prev) => [...prev, { ...newItem, ...createdItem }]);
      } else {
        const createdItem = await handleAIIntegration("/api/create_habit/", {
          description: newItemText,
        });
        setHabits((prev) => [...prev, { ...newItem, ...createdItem }]);
      }

      setNewItemText("");
      setNewItemDeadline("");
      setIsModalOpen(false);
    } catch (error) {
      console.error("Failed to create item", error);
    }
  };

  const toggleComplete = (id: number) => {
    const setter = activeTab === "tasks" ? setTasks : setHabits;
    setter((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, completed: !item.completed } : item,
      ),
    );
  };

  // --- NEW DELETE FUNCTION ---
  const deleteItem = (id: number) => {
    const setter = activeTab === "tasks" ? setTasks : setHabits;
    setter((prev) => prev.filter((item) => item.id !== id));
  };

  const renderContent = () => {
    const currentList = activeTab === "tasks" ? tasks : habits;

    if (currentList.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-full opacity-40 py-10">
          <p className="text-sm text-secondary">
            No {activeTab === "tasks" ? "duties" : "habits"} yet. Click + to
            begin.
          </p>
        </div>
      );
    }

    return (
      <div className="flex flex-col gap-2 pb-4">
        {currentList.map((item) => (
          <div
            key={item.id}
            className={`group flex items-center justify-between gap-3 rounded-lg border p-3 transition-all duration-300 shrink-0 
              ${
                item.completed
                  ? "bg-primary/40 border-slate-900 opacity-50 grayscale-[0.5]"
                  : "bg-primary/80 border-slate-800 animate-in fade-in slide-in-from-left-2"
              }`}
          >
            <div className="flex items-center gap-3 overflow-hidden flex-1">
              <button
                onClick={() => toggleComplete(item.id)}
                className={`w-5 h-5 shrink-0 rounded-full border flex items-center justify-center transition-colors
                  ${
                    item.completed
                      ? "bg-emerald-500/20 border-emerald-500/50 text-emerald-500"
                      : "border-slate-600 hover:border-accent text-transparent hover:text-accent/50"
                  }`}
              >
                <span className="text-[10px]">✓</span>
              </button>

              <div className="flex flex-col truncate">
                <span
                  className={`font-medium text-sm transition-all truncate ${
                    item.completed
                      ? "text-slate-500 line-through"
                      : "text-slate-200"
                  }`}
                >
                  {item.text}
                  <p>STR: {item.strength} INT: {item.intelligence} CHA: {item.charisma}</p>
                </span>
                {item.deadline && (
                  <span className="text-[10px] uppercase tracking-wider text-rose-400/80 font-medium">
                    Due: {item.deadline}
                  </span>
                )}
              </div>
            </div>

            {/* --- DELETE BUTTON --- */}
            <button
              onClick={() => deleteItem(item.id)}
              className="p-1.5 rounded-md text-slate-500 hover:text-rose-500 hover:bg-rose-500/10 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
              title="Delete item"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
              </svg>
            </button>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="w-full h-80 max-h-full rounded-lg border border-slate-800 bg-slate-950/90 shadow-2xl shadow-slate-950/50 backdrop-blur-xl flex flex-col overflow-hidden relative">
      <div className="flex items-center justify-between p-2 border-b border-slate-800 bg-slate-900/50 shrink-0">
        <div className="flex gap-2 grow">
          <button
            onClick={() => setActiveTab("tasks")}
            className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              activeTab === "tasks"
                ? "bg-slate-800 text-accent border border-slate-700 shadow-inner"
                : "text-secondary hover:bg-slate-800/50 hover:text-slate-200 border border-transparent"
            }`}
          >
            Duties
          </button>
          <button
            onClick={() => setActiveTab("habit")}
            className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              activeTab === "habit"
                ? "bg-slate-800 text-accent border border-slate-700 shadow-inner"
                : "text-secondary hover:bg-slate-800/50 hover:text-slate-200 border border-transparent"
            }`}
          >
            Habits
          </button>
        </div>

        <Dialog.Root open={isModalOpen} onOpenChange={setIsModalOpen}>
          <Dialog.Trigger asChild>
            <button className="ml-2 flex items-center justify-center w-10 h-10 rounded-lg bg-accent/10 border border-accent/30 text-accent hover:bg-accent/20 hover:border-accent/50 transition-all active:scale-95 shrink-0">
              <span className="text-2xl">+</span>
            </button>
          </Dialog.Trigger>

          <Dialog.Portal>
            <Dialog.Overlay className="fixed backdrop-blur-sm inset-0 z-40 bg-black/40" />
            <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-white rounded-2xl py-8 px-4 w-[90vw] max-w-md max-h-[90vh] overflow-y-auto border border-gray-500">
              <Dialog.Title
                className={`text-primary text-3xl text-center font-semibold mb-4 ${crossaintOne.className}`}
              >
                New {activeTab === "tasks" ? "Duty" : "Habit"}
              </Dialog.Title>
              <Dialog.Description className="mb-2 text-center text-gray-600">
                {activeTab === "tasks"
                  ? "What one-off thing do you need to get done?"
                  : "What recurring action do you want to build? (resets every day)"}
              </Dialog.Description>

              <div className="flex flex-col">
                <label
                  htmlFor="itemName"
                  className="text-gray-700 text-sm mb-1"
                >
                  Name
                </label>
                <input
                  id="itemName"
                  type="text"
                  className="border rounded-2xl border-gray-500 px-4 py-1 focus:outline-accent mb-4 text-gray-900"
                  placeholder={`E.g., ${
                    activeTab === "tasks"
                      ? "Defeat the Goblin"
                      : "Drink a Potion"
                  }`}
                  value={newItemText}
                  onChange={(e) => setNewItemText(e.target.value)}
                />

                {activeTab === "tasks" && (
                  <>
                    <label
                      htmlFor="itemDeadline"
                      className="text-gray-700 text-sm mb-1"
                    >
                      Deadline
                    </label>
                    <input
                      id="itemDeadline"
                      type="date"
                      min={today}
                      className="border rounded-2xl border-gray-500 px-4 py-1 focus:outline-accent mb-6 text-gray-900"
                      value={newItemDeadline}
                      onChange={(e) => setNewItemDeadline(e.target.value)}
                    />
                  </>
                )}

                <Button
                  variant="default"
                  size="default"
                  onClick={handleAdd}
                  disabled={!newItemText.trim()}
                >
                  Save {activeTab === "tasks" ? "Duty" : "Habit"}
                </Button>
              </div>
            </Dialog.Content>
          </Dialog.Portal>
        </Dialog.Root>
      </div>

      <div className="flex-1 p-4 overflow-y-auto overflow-x-hidden custom-scrollbar">
        {renderContent()}
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #1e293b;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #334155;
        }
      `}</style>
    </div>
  );
}

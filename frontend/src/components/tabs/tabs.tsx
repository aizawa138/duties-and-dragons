"use client";
import { useState } from "react";


export default function Tabs() {
    const [activeTab, setActiveTab] = useState("tab1");

    const tabs = [
        { id: "tasks", label: "Tasks", content: <p>Tasks Tab</p>},
        { id: "habit", label: "Habit", content: <p>Habits Tab</p>},
    ];

    return (
        <div className="mt-10">
            <div className="flex w-full">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 w-full ${activeTab === tab.id ? "bg-primary text-white" : "bg-secondary"}`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className="p-4">
                {tabs.find((tab) => tab.id === activeTab)?.content}
            </div>
        </div>
    );
}
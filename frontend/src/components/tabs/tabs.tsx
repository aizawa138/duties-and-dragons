"use client";
import { useState } from "react";

export default function Tabs() {
    const [activeTab, setActiveTab] = useState("tasks");

    const tabs = [
        { id: "tasks", label: "Duties", content: <p className="text-sm text-secondary italic">No duties yet. Click the + to begin.</p>},
        { id: "habit", label: "Habits", content: <p className="text-sm text-secondary italic">No habits tracked yet.</p>},
    ];

    const handleAdd = () => {
        console.log(`Adding new item to: ${activeTab}`);
        // This is where you'd trigger a modal or a new row
    };

    return (
        <div className="w-full h-full rounded-lg border border-slate-800 bg-slate-950/90 shadow-2xl shadow-slate-950/50 backdrop-blur-xl flex flex-col overflow-hidden">
            {/* Header Row */}
            <div className="flex items-center justify-between p-2 border-b border-slate-800 bg-slate-900/50">
                
                {/* Tab Switchers */}
                <div className="flex gap-2 grow">
                    {tabs.map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                                activeTab === tab.id 
                                    ? "bg-slate-800 text-accent border border-slate-700 shadow-inner" 
                                    : "text-secondary hover:bg-slate-800/50 hover:text-slate-200 border border-transparent"
                            }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* The "Plus" Action Button */}
                <button 
                    onClick={handleAdd}
                    className="ml-2 flex items-center justify-center w-10 h-10 rounded-lg bg-accent/10 border border-accent/30 text-accent hover:bg-accent/20 hover:border-accent/50 transition-all active:scale-95 group"
                    title={`Add ${activeTab === 'tasks' ? 'Task' : 'Habit'}`}
                >
                    <span className="text-2xl">+</span>
                </button>
            </div>
            
            {/* Content Area */}
            <div className="p-6 grow overflow-y-auto">
                {tabs.find((tab) => tab.id === activeTab)?.content}
            </div>
        </div>
    );
}
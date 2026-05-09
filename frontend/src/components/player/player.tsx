interface PlayerProps {
    s: string;
}

export default function Player({ s }: PlayerProps) {
    return (
        <div className="w-full h-[30vh] flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <span className="text-[0.8vw] uppercase tracking-[0.2em] text-secondary mb-2">Character</span>
            <div className="font-semibold text-[1vw] text-accent">
                I'm {s}.
            </div>
        </div>
    );
}
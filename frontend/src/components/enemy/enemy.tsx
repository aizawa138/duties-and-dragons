interface EnemyProps {
    s: string;
}

export default function Enemy({ s }: EnemyProps) {
    return (
        <div className="w-full h-[30vh] flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <span className="text-xs uppercase tracking-[0.2em] text-secondary mb-2">Current Target</span>
            <div className="font-semibold text-lg text-red-400/90">
                I'm {s}!
            </div>
        </div>
    );
}
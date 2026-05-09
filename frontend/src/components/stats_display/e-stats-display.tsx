interface StatsInfo {
    hp: number;
    weakness: string;
}

export default function EnemyStats({ hp, weakness }: StatsInfo) {
    return (
        <div className="w-full h-[30vh] text-center flex flex-col items-center justify-center rounded-lg p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <ul className="flex flex-col gap-5">
                <li>HP: {hp}</li>
                <li>Weak to: {weakness}</li>
            </ul>
        </div>
    );
}
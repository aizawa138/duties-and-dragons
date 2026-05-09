interface StatsInfo {
    hp: number;
    id: number;
    time_left: number;
}

export default function EnemyStats({ hp, id, time_left }: StatsInfo) {
    if (id === 1) {
        var weakness = "STR";
    } else if (id === 2) {
        var weakness = "INT";
    } else {
        var weakness = "CHA";
    }

    return (
        <div className="w-full h-[30vh] text-center flex flex-col items-center justify-center rounded-lg p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <ul className="flex flex-col gap-5">
                <li>HP: {hp}</li>
                <li>Weak to: {weakness}</li>
                <li>Time left: {time_left}</li>
            </ul>
        </div>
    );
}
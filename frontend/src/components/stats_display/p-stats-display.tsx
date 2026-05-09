interface StatsInfo {
    str: number;
    int: number;
    cha: number;
    hp: number;
    level: number;
}

export default function PlayerStats({ str, int, cha, hp, level }: StatsInfo) {
    return (
        <div className="w-full h-[30vh] text-center flex flex-col items-center justify-center rounded-lg p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <ul className="flex flex-col gap-2">
                <li>Level: {level}</li>
                <li>EXP: {(str + int + cha).toFixed(2)}</li>
                <li>HP: {hp.toFixed(2)}</li>
                <li>STR: {str.toFixed(2)}</li>
                <li>INT: {int.toFixed(2)}</li>
                <li>CHA: {cha.toFixed(2)}</li>
            </ul>
        </div>
    );
}
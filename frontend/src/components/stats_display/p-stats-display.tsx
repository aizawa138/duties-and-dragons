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
                <li>EXP: {str + int + cha}</li>
                <li>HP: {hp}</li>
                <li>STR: {str}</li>
                <li>INT: {int}</li>
                <li>CHA: {cha}</li>
            </ul>
        </div>
    );
}
import Knight from "@/public/knight.png";
import Mage from "@/public/mage.png";
import Vampire from "@/public/vampire.png";
import Image from 'next/image';

interface PlayerClass {
    s: string;
}

const classes: { [key: string]: any } = {
    "Knight": Knight,
    "Mage": Mage,
    "Vampire": Vampire,
}

export default function Player({ s }: PlayerClass) {
    return (
        <div className="w-full h-[30vh] flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <span className="text-[0.8vw] uppercase tracking-[0.2em] text-secondary mb-2">Character</span>
            <div className="font-semibold text-[1vw] text-accent animate-bob">
                <Image src={classes[s]} alt="Player" />
            </div>
        </div>
    );
}
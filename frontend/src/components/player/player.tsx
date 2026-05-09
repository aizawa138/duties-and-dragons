import knight from "@/public/knight.png";
import mage from "@/public/mage.png";
import vampire from "@/public/vampire.png";
import Image from 'next/image';

interface PlayerClass {
    s: string;
}

export default function Player({ s }: PlayerClass) {
    return (
        <div className="w-full h-[30vh] flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <span className="text-[0.8vw] uppercase tracking-[0.2em] text-secondary mb-2">Character</span>
            <div className="font-semibold text-[1vw] text-accent animate-bob">
                <Image src={knight} alt="Player" />
            </div>
        </div>
    );
}
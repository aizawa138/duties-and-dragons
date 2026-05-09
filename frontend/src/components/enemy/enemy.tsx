import redd from '@/public/redd.png';
import purpled from '@/public/purpled.png';
import whited from '@/public/whited.png';
import Image from 'next/image';

interface EnemyProps {
    s: number;
}

const types: { [key: number]: any } = {
    1: redd,
    2: purpled,
    3: whited,
}

export default function Enemy({ s }: EnemyProps) {
    return (
        <div className="w-full h-[30vh] flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl shrink-0">
            <span className="text-[0.8vw] uppercase tracking-[0.2em] text-secondary mb-2">Current Target</span>
            <div className="font-semibold text-[1vw] text-red-400/90">
            <Image src={types[s]} alt="Enemy" className="scale-x-[-1] animate-bob"/>
            </div>
        </div>
    );
}
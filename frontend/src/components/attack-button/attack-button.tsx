interface AttackButtonProps {
    onAttack: () => void;
}

export default function AttackButton({ onAttack }: AttackButtonProps) {
    return (
        <button 
            onClick={onAttack}
            className="flex justify-center items-center bg-red-600 h-full w-full hover:bg-red-400 text-white font-bold text-[1vw] py-2 px-6 border-b-4 border-red-800 hover:border-red-600 rounded active:border-b-0 active:mt-1"
        >
            ATTACK
        </button>
    );
}
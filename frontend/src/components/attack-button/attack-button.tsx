interface AttackButtonProps {
    onAttack: () => void;
}

export default function AttackButton({ onAttack }: AttackButtonProps) {
    return (
        <button 
            onClick={onAttack}
            className="flex justify-center aspect-square items-center bg-red-900 w-full hover:bg-red-800 text-white font-bold text-[1vw] py-2 px-6 border-b-4 border-red-950 hover:border-red-750 rounded active:border-b-0 active:mt-1"
        >
            ATTACK
        </button>
    );
}
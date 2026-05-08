import { Button } from "../ui/button/button";
import Logo from "../logo/Logo";

export default function Header() {
    return (<header className="flex justify-end items-center p-4 bg-state-900 text-white bg-primary">
        <div className="flex-1"></div>
        <div className="flex-1 text-center font-bold"><Logo /></div>
        <div className="flex-1 text-right"><Button variant="secondary" size="default" className="bg-secondary">Log In</Button></div>
    </header>);
}
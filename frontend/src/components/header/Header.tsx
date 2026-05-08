import LoginModal from "@/src/features/login/LoginModal";
import Logo from "../logo/Logo";

export default function Header() {
  return (
    <header className="sticky top-0 flex justify-end items-center p-4 bg-state-900 text-white bg-primary h-16">
      <div className="flex-1"></div>
      <div className="flex-1 text-center font-bold">
        <Logo />
      </div>
      <div className="flex-1 text-right">
        <LoginModal authenticationType="Login" variant="default" />
        <LoginModal authenticationType="Signup" variant="secondary" />
      </div>
    </header>
  );
}

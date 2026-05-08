import Link from "next/link";
import { crossaintOne } from "@/public/fonts";

export default function Logo() {
  return (
    <Link href="/" className={`${crossaintOne.className} text-3xl text-accent`}>
      Duties & Dragons
    </Link>
  );
}

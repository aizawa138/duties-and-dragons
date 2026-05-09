import Link from "next/link";
import { crossaintOne } from "@/public/fonts";

type LogoProps = {
  href?: string;
};

export default function Logo({ href = "/" }: LogoProps) {
  return (
    <Link href={href} className={`${crossaintOne.className} text-3xl text-accent`}>
      Duties & Dragons
    </Link>
  );
}

import Image, { StaticImageData } from "next/image";

type CardProps = {
  src: StaticImageData;
  role: string;
};

export default function Card({ src, role }: CardProps) {
  return (
    <div className="group border border-accent bg-primary rounded-2xl p-4 overflow-hidden hover:cursor-pointer">
      <Image
        src={src}
        alt="Image of the classes"
        height={250}
        width={250}
        loading="eager"
        className="group-hover:scale-110 transition mb-2"
      />
      <h1 className="text-3xl text-background mb-2 font-bold">{role}</h1>
      <p className="text-gray-400">Good morning to 9/5</p>
    </div>
  );
}

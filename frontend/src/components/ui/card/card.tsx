import Image, { StaticImageData } from "next/image";

type CardProps = {
  src: StaticImageData;
  role: string;
  onClick: (value: string) => void;
  isSelected?: boolean;
  description: string;
};

export default function Card({
  src,
  role,
  onClick,
  isSelected,
  description,
}: CardProps) {
  const selectedClasses = isSelected ? "scale-[1.02] ring-2 ring-accent" : "";
  return (
    <div
      className={`group border-2 border-accent bg-primary rounded-2xl p-4 overflow-hidden hover:cursor-pointer transition ${selectedClasses}`}
      onClick={() => onClick(role)}
    >
      <div className="flex justify-center mb-2">
        <Image
          src={src}
          alt="Image of the classes"
          height={250}
          width={250}
          loading="eager"
          className={`transition mb-2${isSelected ? "scale-110" : "group-hover:scale-110"}`}
        />
      </div>
      <h1 className="text-3xl text-background mb-2 font-bold">{role}</h1>
      <p className="text-gray-400">{description}</p>
    </div>
  );
}

import { alikeAngular, crossaintOne } from "@/public/fonts";

export default function LandingPage() {
  return (
    <div
      className={`min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}
    >
      {/* Cinematic Background */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 px-6 flex flex-col items-center text-center">
        <span
          className={`text-xs ${alikeAngular.className} tracking-widest uppercase text-secondary mb-3`}
        >
          The Ultimate Gamified Task Experience
        </span>

        <h1
          className={`text-6xl md:text-8xl ${crossaintOne.className} tracking-tighter text-accent`}
        >
          Duties <span className="text-accent">&</span> Dragons
        </h1>

        <p
          className={`${alikeAngular.className} mt-6 max-w-2xl text-lg md:text-xl text-secondary leading-relaxed`}
        >
          Set the tasks you need completed. Complete them to power up your
          character. Defeat monsters with your productivity. Don't die.
        </p>
      </section>
      {/* Feature Grid */}
      <section className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            title="AI Dungeon Master"
            desc="A special fine-tuned AI unit analyses the tasks you add to determine their difficulty and rewards you get upon their completion."
          />
          <FeatureCard
            title="Survive the Week"
            desc="A special boss monster appears every week. Complete your tasks to deplete its HP. If the boss is not defeated by the end of the week, it strikes back."
          />
          <FeatureCard
            title="Claim Your Glory"
            desc="Climb the global leaderboard. Complete more tasks, defeat more bosses, and earn more glory while becoming even more prductive."
          />
        </div>
      </section>

      {/* The "Permadeath" Warning */}
      <section className="relative z-10 py-20 bg-linear-to-b from-transparent via-red-950/10 to-transparent">
        <div className="max-w-4xl mx-auto text-center px-6">
          <div className="inline-block p-4 border-2 border-red-900 bg-red-950/20 backdrop-blur-md rounded-lg">
            <h2 className="text-3xl font-bold text-red-500 uppercase tracking-tighter mb-4">
              WARNING
            </h2>
            <p className="text-secondary leading-relaxed">
              You complete your tasks to survive. The more weekly bosses you
              fail to defeat, the more HP you lose. Lose all your HP, and it's
              game over. All your progress and gathered glory will be lost
              forever.
              <br></br>Procrastination has consequences.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="p-8 bg-slate-900/50 border border-slate-800 rounded-lg">
      <h3
        className={`text-xl ${crossaintOne.className} text-accent mb-2 uppercase tracking-tight`}
      >
        {title}
      </h3>
      <p
        className={`${alikeAngular.className} text-secondary text-sm leading-relaxed`}
      >
        {desc}
      </p>
    </div>
  );
}

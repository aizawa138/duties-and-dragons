import Header from "@/src/components/header/Header";
import DashboardBack from "@/src/components/dashboard-back/dashboard-back";

export default async function Page({ params }: { params: { username: string } }) {
    const { username } = await params;
    return (
      <main className="relative">
        <Header />
        <DashboardBack />
        <p>Welcome to the dashboard: {username}</p>
      </main>
    );
  }
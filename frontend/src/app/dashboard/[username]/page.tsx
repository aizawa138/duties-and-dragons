import ProtectedDashboard from "@/src/components/dashboard-back/protected-dashboard";

type DashboardPageProps = {
  params: Promise<{ username: string }>;
};

export default async function Page({ params }: DashboardPageProps) {
  const { username } = await params;

  return <ProtectedDashboard username={username} />;
}

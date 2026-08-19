"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchCurrentUser, clearTokens, type CurrentUser } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCurrentUser().then((currentUser) => {
      if (!currentUser) {
        router.replace("/");
        return;
      }
      setUser(currentUser);
      setLoading(false);
    });
  }, [router]);

  function handleLogout() {
    clearTokens();
    router.replace("/");
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-neutral-950 text-white">
        <p className="text-neutral-400">Carregando...</p>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-neutral-950 text-white px-4">
      {user?.avatar_url && (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={user.avatar_url}
          alt={user.nome}
          className="w-20 h-20 rounded-full border-2 border-neutral-700"
        />
      )}
      <div className="text-center">
        <h1 className="text-2xl font-bold">Bem-vindo, {user?.nome}!</h1>
        <p className="text-neutral-400">{user?.email}</p>
      </div>

      <p className="text-sm text-neutral-500 max-w-md text-center">
        Isso confirma que o login está funcionando de ponta a ponta: Google →
        Backend → JWT → Frontend.
      </p>

      <button
        onClick={handleLogout}
        className="text-sm text-neutral-500 hover:text-red-400 underline"
      >
        Sair
      </button>
    </main>
  );
}

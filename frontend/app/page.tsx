import Link from "next/link";
import { getGoogleLoginUrl } from "@/lib/auth";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-neutral-950 text-white px-4">
      <h1 className="text-4xl font-bold tracking-tight">
        Dex<span className="text-red-500">Forge</span>
      </h1>
      <p className="text-neutral-400 text-center max-w-md">
        Uma Pokédex completa — busca, coleção pessoal, comparador e muito
        mais. Projeto em construção. 🚧
      </p>

      <a
        href={getGoogleLoginUrl()}
        className="flex items-center gap-3 bg-white text-neutral-900 font-medium px-6 py-3 rounded-lg hover:bg-neutral-200 transition-colors"
      >
        Entrar com Google
      </a>

      <Link
        href="/dashboard"
        className="text-sm text-neutral-500 hover:text-neutral-300 underline"
      >
        Já tenho uma sessão ativa →
      </Link>
    </main>
  );
}

"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { saveTokens } from "@/lib/auth";

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const accessToken = searchParams.get("access_token");
  const refreshToken = searchParams.get("refresh_token");
  const hasError = !accessToken || !refreshToken;

  useEffect(() => {
    if (hasError || !accessToken || !refreshToken) return;

    saveTokens(accessToken, refreshToken);
    router.replace("/dashboard");
  }, [hasError, accessToken, refreshToken, router]);

  if (hasError) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-neutral-950 text-white px-4">
        <p className="text-red-400">
          Não recebemos os tokens esperados do servidor.
        </p>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-neutral-950 text-white">
      <p className="text-neutral-400">Finalizando login...</p>
    </main>
  );
}
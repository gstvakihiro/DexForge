/**
 * Funções utilitárias de autenticação.
 *
 * Por enquanto guardamos os tokens no localStorage — simples e suficiente
 * pra validar o fluxo. Numa fase futura, o ideal é mover o refresh_token
 * pra um cookie httpOnly (mais seguro contra ataques XSS).
 */

const ACCESS_TOKEN_KEY = "dexforge_access_token";
const REFRESH_TOKEN_KEY = "dexforge_refresh_token";

export function saveTokens(accessToken: string, refreshToken: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export function isLoggedIn(): boolean {
  return getAccessToken() !== null;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export interface CurrentUser {
  id: string;
  email: string;
  nome: string;
  avatar_url: string | null;
  created_at: string;
}

/**
 * Busca os dados do usuário logado, usando o token salvo.
 * Devolve null se não estiver logado ou se o token for inválido.
 */
export async function fetchCurrentUser(): Promise<CurrentUser | null> {
  const token = getAccessToken();
  if (!token) return null;

  const response = await fetch(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    clearTokens();
    return null;
  }

  return response.json();
}

/**
 * Monta a URL que inicia o login com Google (redireciona pro backend).
 */
export function getGoogleLoginUrl(): string {
  return `${API_URL}/auth/google/login`;
}

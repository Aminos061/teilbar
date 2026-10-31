import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { supabaseEnv } from "./env";

// Für Server Components, Server Actions und Route Handlers. Pro Anfrage ein neuer Client,
// weil er die Cookies dieser Anfrage braucht.
// Sobald es eine Anmeldung gibt, braucht es zusätzlich eine proxy.ts, die die Sitzung auffrischt
// (Supabase: https://supabase.com/docs/guides/auth/server-side/nextjs). Bis dahin schlägt das
// Schreiben der Cookies in Server Components still fehl.
export async function createClient() {
  const cookieStore = await cookies();
  const { url, key } = supabaseEnv();
  return createServerClient(url, key, {
    cookies: {
      getAll: () => cookieStore.getAll(),
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
        } catch {
          // In Server Components nicht erlaubt; ein Proxy übernimmt das Schreiben.
        }
      },
    },
  });
}

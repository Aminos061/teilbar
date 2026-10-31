// NEXT_PUBLIC_*-Variablen müssen wörtlich stehen, sonst ersetzt Next.js sie nicht im Browser-Bundle.
export function supabaseEnv() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;
  if (!url || !key) {
    throw new Error(
      "NEXT_PUBLIC_SUPABASE_URL und NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY fehlen. Vorlage: web/.env.example",
    );
  }
  return { url, key };
}

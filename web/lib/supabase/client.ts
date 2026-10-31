import { createBrowserClient } from "@supabase/ssr";
import { supabaseEnv } from "./env";

// Für Client Components. Der Publishable Key ist für den Browser gedacht; den Schutz der Daten
// leisten die Row-Level-Security-Regeln in web/supabase/migrations/.
export function createClient() {
  const { url, key } = supabaseEnv();
  return createBrowserClient(url, key);
}

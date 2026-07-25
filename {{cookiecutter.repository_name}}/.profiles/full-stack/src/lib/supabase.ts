import { createClient } from "@supabase/supabase-js";

import type { Database } from "../types/database";

const url = import.meta.env.VITE_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey =
  import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY ??
  "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH";

export const supabase = createClient<Database>(url, publishableKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
  },
});

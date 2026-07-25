import { createClient, type SupabaseClient } from "@supabase/supabase-js";

import type { Database } from "../../types/database";

const url = process.env.VITE_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey =
  process.env.VITE_SUPABASE_PUBLISHABLE_KEY ??
  "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH";

export const USERS = {
  owner: {
    id: "00000000-0000-0000-0000-000000000001",
    email: "owner@example.test",
  },
  outsider: {
    id: "00000000-0000-0000-0000-000000000002",
    email: "outsider@example.test",
  },
} as const;

const password = "local-password-123";

export async function signInAs(
  role: keyof typeof USERS,
): Promise<SupabaseClient<Database>> {
  const client = createClient<Database>(url, publishableKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  const { error } = await client.auth.signInWithPassword({
    email: USERS[role].email,
    password,
  });
  if (error) throw new Error(`local seed sign-in failed: ${error.message}`);
  return client;
}

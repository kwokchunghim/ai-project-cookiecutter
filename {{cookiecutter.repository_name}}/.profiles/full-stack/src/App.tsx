import type { Session } from "@supabase/supabase-js";
import { type FormEvent, useEffect, useState } from "react";

import { normalizeDisplayName, profileLabel } from "./lib/profile";
import { supabase } from "./lib/supabase";

const PROJECT_NAME = "{{ cookiecutter.project_name }}";

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [displayName, setDisplayName] = useState<string | null>(null);
  const [draftName, setDraftName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"sign-in" | "sign-up">("sign-in");
  const [message, setMessage] = useState("");

  useEffect(() => {
    void supabase.auth
      .getSession()
      .then(({ data }) => setSession(data.session));
    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
    });
    return () => data.subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (!session) {
      return;
    }
    void supabase
      .from("profiles")
      .select("display_name")
      .eq("id", session.user.id)
      .single()
      .then(({ data, error }) => {
        if (error) {
          setMessage(error.message);
          return;
        }
        setDisplayName(data.display_name);
        setDraftName(data.display_name ?? "");
      });
  }, [session]);

  async function authenticate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    const result =
      mode === "sign-in"
        ? await supabase.auth.signInWithPassword({ email, password })
        : await supabase.auth.signUp({
            email,
            password,
            options: { data: { display_name: email.split("@")[0] } },
          });
    setMessage(
      result.error?.message ?? (mode === "sign-up" ? "Account created." : ""),
    );
  }

  async function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session) return;

    try {
      const normalized = normalizeDisplayName(draftName);
      const { error } = await supabase
        .from("profiles")
        .update({
          display_name: normalized,
          updated_at: new Date().toISOString(),
        })
        .eq("id", session.user.id);
      if (error) throw error;
      setDisplayName(normalized);
      setMessage("Profile saved.");
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Unable to save profile.",
      );
    }
  }

  if (!session) {
    return (
      <main className="mx-auto flex min-h-screen max-w-md items-center px-6">
        <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <p className="text-sm font-semibold text-indigo-600">
            {PROJECT_NAME}
          </p>
          <h1 className="mt-2 text-2xl font-semibold">
            {mode === "sign-in" ? "Sign in" : "Create account"}
          </h1>
          <form
            className="mt-6 grid gap-4"
            onSubmit={(event) => void authenticate(event)}
          >
            <input
              className="rounded-lg border border-slate-300 px-3 py-2"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
            />
            <input
              className="rounded-lg border border-slate-300 px-3 py-2"
              type="password"
              minLength={8}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Password"
              required
            />
            <button
              className="rounded-lg bg-indigo-600 px-4 py-2 text-white"
              type="submit"
            >
              {mode === "sign-in" ? "Sign in" : "Sign up"}
            </button>
          </form>
          <button
            className="mt-4 text-sm text-indigo-700"
            type="button"
            onClick={() => setMode(mode === "sign-in" ? "sign-up" : "sign-in")}
          >
            {mode === "sign-in"
              ? "Need an account?"
              : "Already have an account?"}
          </button>
          {message && <p className="mt-4 text-sm text-slate-700">{message}</p>}
        </section>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-16">
      <p className="text-sm font-semibold text-indigo-600">{PROJECT_NAME}</p>
      <h1 className="mt-2 text-3xl font-semibold">
        Hello, {profileLabel(displayName, session.user.email ?? "user")}
      </h1>
      <form
        className="mt-8 grid max-w-md gap-4"
        onSubmit={(event) => void saveProfile(event)}
      >
        <label className="grid gap-2">
          <span className="text-sm font-medium">Display name</span>
          <input
            className="rounded-lg border border-slate-300 px-3 py-2"
            value={draftName}
            onChange={(event) => setDraftName(event.target.value)}
          />
        </label>
        <button
          className="rounded-lg bg-indigo-600 px-4 py-2 text-white"
          type="submit"
        >
          Save profile
        </button>
      </form>
      <button
        className="mt-6 text-sm text-indigo-700"
        type="button"
        onClick={() => void supabase.auth.signOut()}
      >
        Sign out
      </button>
      {message && <p className="mt-4 text-sm text-slate-700">{message}</p>}
    </main>
  );
}

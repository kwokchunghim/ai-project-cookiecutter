import { describe, expect, it } from "vitest";

import { signInAs, USERS } from "./client";

describe("profiles ownership RLS", () => {
  it("lets the owner read and update their profile", async () => {
    const client = await signInAs("owner");
    const { data: visible, error: selectError } = await client
      .from("profiles")
      .select("id, display_name");

    expect(selectError).toBeNull();
    expect(visible).toEqual([
      { id: USERS.owner.id, display_name: "Seed Owner" },
    ]);

    const { data: updated, error: updateError } = await client
      .from("profiles")
      .update({ display_name: "Owner Updated" })
      .eq("id", USERS.owner.id)
      .select("display_name");

    expect(updateError).toBeNull();
    expect(updated).toEqual([{ display_name: "Owner Updated" }]);
  });

  it("hides an owner's profile from an authenticated outsider", async () => {
    const client = await signInAs("outsider");
    const { data, error } = await client
      .from("profiles")
      .select("id")
      .eq("id", USERS.owner.id);

    expect(error).toBeNull();
    expect(data).toEqual([]);
  });

  it("denies outsider updates through the update USING policy", async () => {
    const client = await signInAs("outsider");
    const { data, error } = await client
      .from("profiles")
      .update({ display_name: "Compromised" })
      .eq("id", USERS.owner.id)
      .select("id");

    expect(error).toBeNull();
    expect(data).toEqual([]);
  });
});

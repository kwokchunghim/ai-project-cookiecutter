import { describe, expect, it } from "vitest";

import { normalizeDisplayName, profileLabel } from "./profile";

describe("normalizeDisplayName", () => {
  it("trims and collapses whitespace before persistence", () => {
    expect(normalizeDisplayName("  Ada   Lovelace ")).toBe("Ada Lovelace");
  });

  it("rejects names outside the database constraint", () => {
    expect(() => normalizeDisplayName("x")).toThrow("2-80 characters");
    expect(() => normalizeDisplayName("x".repeat(81))).toThrow(
      "2-80 characters",
    );
  });
});

describe("profileLabel", () => {
  it("falls back to the authenticated email when no display name exists", () => {
    expect(profileLabel(null, "owner@example.test")).toBe("owner@example.test");
    expect(profileLabel("Owner", "owner@example.test")).toBe("Owner");
  });
});

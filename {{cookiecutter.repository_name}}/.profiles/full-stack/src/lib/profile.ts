export const MIN_DISPLAY_NAME_LENGTH = 2;
export const MAX_DISPLAY_NAME_LENGTH = 80;

export function normalizeDisplayName(value: string): string {
  const normalized = value.trim().replace(/\s+/g, " ");
  if (
    normalized.length < MIN_DISPLAY_NAME_LENGTH ||
    normalized.length > MAX_DISPLAY_NAME_LENGTH
  ) {
    throw new Error(
      `Display name must be ${MIN_DISPLAY_NAME_LENGTH}-${MAX_DISPLAY_NAME_LENGTH} characters.`,
    );
  }
  return normalized;
}

export function profileLabel(
  displayName: string | null,
  email: string,
): string {
  return displayName?.trim() || email;
}

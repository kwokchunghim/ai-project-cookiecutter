#!/bin/sh
set -eu

temporary_directory="$(mktemp -d)"
temporary_types="$temporary_directory/database.ts"
cleanup() {
  rm -f "$temporary_types"
  rmdir "$temporary_directory"
}
trap cleanup EXIT HUP INT TERM

attempt=1
max_attempts=4
until npm exec -- supabase gen types typescript --local > "$temporary_types"; do
  if [ "$attempt" -eq "$max_attempts" ]; then
    echo "Supabase type generation failed after $max_attempts attempts." >&2
    exit 1
  fi

  delay=$((attempt * 5))
  echo "Supabase type generation failed; retrying in ${delay}s." >&2
  sleep "$delay"
  attempt=$((attempt + 1))
done

npm exec -- prettier --write "$temporary_types"
diff -u src/types/database.ts "$temporary_types"

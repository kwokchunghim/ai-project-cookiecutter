#!/bin/sh
set -eu

temporary_directory="$(mktemp -d)"
temporary_types="$temporary_directory/database.ts"
cleanup() {
  rm -f "$temporary_types"
  rmdir "$temporary_directory"
}
trap cleanup EXIT HUP INT TERM

npm exec -- supabase gen types typescript --local > "$temporary_types"
npm exec -- prettier --write "$temporary_types"
diff -u src/types/database.ts "$temporary_types"

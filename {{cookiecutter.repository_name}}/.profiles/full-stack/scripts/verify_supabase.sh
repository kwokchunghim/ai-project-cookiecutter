#!/bin/sh
set -eu

cleanup() {
  npm exec -- supabase stop --no-backup
}
trap cleanup EXIT HUP INT TERM

npm exec -- supabase start
npm exec -- supabase db reset
npm run test:rls
./scripts/check_database_types.sh

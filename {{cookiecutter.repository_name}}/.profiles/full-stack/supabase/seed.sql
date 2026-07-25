-- Deterministic local-only users for owner/outsider RLS verification.
insert into auth.users (
  instance_id,
  id,
  aud,
  role,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  raw_app_meta_data,
  raw_user_meta_data,
  is_super_admin,
  confirmation_token,
  recovery_token,
  email_change_token_new,
  email_change,
  email_change_token_current,
  phone_change,
  phone_change_token,
  reauthentication_token
)
select
  '00000000-0000-0000-0000-000000000000',
  seed.id,
  'authenticated',
  'authenticated',
  seed.email,
  extensions.crypt('local-password-123', extensions.gen_salt('bf')),
  now(),
  now(),
  now(),
  '{"provider":"email","providers":["email"]}'::jsonb,
  jsonb_build_object('display_name', seed.display_name),
  false,
  '',
  '',
  '',
  '',
  '',
  '',
  '',
  ''
from (
  values
    (
      '00000000-0000-0000-0000-000000000001'::uuid,
      'owner@example.test',
      'Seed Owner'
    ),
    (
      '00000000-0000-0000-0000-000000000002'::uuid,
      'outsider@example.test',
      'Seed Outsider'
    )
) as seed (id, email, display_name);

insert into auth.identities (
  id,
  provider_id,
  user_id,
  identity_data,
  provider,
  last_sign_in_at,
  created_at,
  updated_at
)
select
  extensions.gen_random_uuid(),
  users.id::text,
  users.id,
  jsonb_build_object(
    'sub', users.id::text,
    'email', users.email,
    'email_verified', true
  ),
  'email',
  now(),
  now(),
  now()
from auth.users as users
where users.email in ('owner@example.test', 'outsider@example.test');

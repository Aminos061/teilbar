-- Profil je Konto (docs/adr/0007-tech-stack-der-app.md).
-- Row Level Security von Anfang an: Der Browser greift direkt auf die Datenbank zu.
-- Sichtbarkeit für Nachbarn (Vertrauensstufen, Hausbuch) kommt mit späteren Migrationen.

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Eigenes Profil lesen"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = id);

create policy "Eigenes Profil ändern"
  on public.profiles for update
  to authenticated
  using ((select auth.uid()) = id)
  with check ((select auth.uid()) = id);

-- Kein insert- und kein delete-Recht für Nutzer: Angelegt wird das Profil vom Trigger unten,
-- gelöscht wird es mit dem Konto (on delete cascade).

create function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id) values (new.id);
  return new;
end;
$$;

revoke execute on function public.handle_new_user() from public, anon, authenticated;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

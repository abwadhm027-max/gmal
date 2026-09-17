create extension if not exists "pgcrypto";

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null default '',
  role text not null default 'jobseeker' check (role in ('jobseeker','employer','admin')),
  created_at timestamptz not null default now()
);

create table if not exists public.jobs (
  id uuid primary key default gen_random_uuid(),
  employer_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  company text not null,
  city text not null,
  description text not null,
  salary_min integer,
  salary_max integer,
  created_at timestamptz not null default now()
);

create table if not exists public.applications (
  id uuid primary key default gen_random_uuid(),
  job_id uuid not null references public.jobs(id) on delete cascade,
  applicant_id uuid not null references public.profiles(id) on delete cascade,
  message text default '',
  status text not null default 'pending' check (status in ('pending','reviewed','accepted','rejected')),
  created_at timestamptz not null default now(),
  unique(job_id, applicant_id)
);

alter table public.profiles enable row level security;
alter table public.jobs enable row level security;
alter table public.applications enable row level security;

create policy "profiles_read_own" on public.profiles
for select using (auth.uid() = id);

create policy "profiles_insert_own" on public.profiles
for insert with check (auth.uid() = id);

create policy "jobs_public_read" on public.jobs
for select using (true);

create policy "jobs_employer_insert" on public.jobs
for insert with check (auth.uid() = employer_id);

create policy "jobs_employer_update" on public.jobs
for update using (auth.uid() = employer_id);

create policy "jobs_employer_delete" on public.jobs
for delete using (auth.uid() = employer_id);

create policy "applications_insert_own" on public.applications
for insert with check (auth.uid() = applicant_id);

create policy "applications_read_own" on public.applications
for select using (auth.uid() = applicant_id);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', ''));
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();

insert into public.jobs (employer_id, title, company, city, description, salary_min, salary_max)
select id, 'موظف مبيعات', 'IraqJobs Demo', 'بغداد', 'وظيفة تجريبية للتأكد من اتصال التطبيق بقاعدة البيانات.', 500000, 750000
from public.profiles
where role = 'admin'
limit 1;

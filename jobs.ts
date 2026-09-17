import { supabase } from "./supabase";

export type Job = {
  id: string;
  title: string;
  company: string;
  city: string;
  description: string;
  salary_min: number | null;
  salary_max: number | null;
  created_at: string;
};

export async function getJobs(search = "") {
  let query = supabase
    .from("jobs")
    .select("*")
    .order("created_at", { ascending: false });

  if (search.trim()) {
    const q = search.trim().replace(/,/g, " ");
    query = query.or(`title.ilike.%${q}%,company.ilike.%${q}%,city.ilike.%${q}%`);
  }

  const { data, error } = await query;
  if (error) throw error;
  return (data ?? []) as Job[];
}

export async function createJob(input: {
  title: string;
  company: string;
  city: string;
  description: string;
  salary_min?: number;
  salary_max?: number;
}) {
  const { data: auth } = await supabase.auth.getUser();
  if (!auth.user) throw new Error("يجب تسجيل الدخول أولاً");

  const { data, error } = await supabase
    .from("jobs")
    .insert({ ...input, employer_id: auth.user.id })
    .select()
    .single();

  if (error) throw error;
  return data as Job;
}

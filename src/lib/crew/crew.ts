import { createClient } from '@supabase/supabase-js';
import { Activity } from '../../types/activity';

// Initialisation Supabase (utilise les variables d'env)
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Agent 1 : Extraction des critères
export async function TripRequestParser(input: string): Promise<{
  city: string;
  dates?: string;
  categories?: string[];
  budget?: string;
  mood?: string;
}> {
  // Prompt minimaliste, à remplacer par un LLM plus tard si besoin
  // Ici, simple parsing regex pour l'exemple
  const cityMatch = input.match(/à ([a-zA-Zéèêëîïôöùûüç\s]+?)(?:\s+avec|\s*$)/i);
  const budgetMatch = input.match(/(petit|moyen|grand) budget/i);
  const moodMatch = input.match(/(romantique|aventure|détente|culturel|festif)/i);

  return {
    city: cityMatch ? cityMatch[1].trim() : '',
    budget: budgetMatch ? budgetMatch[1] : undefined,
    mood: moodMatch ? moodMatch[1] : undefined,
    // Ajoute d'autres extractions si besoin
  };
}

// Agent 2 : Recherche Supabase
export async function SupabaseSearchAgent(criteria: {
  city: string;
  budget?: string;
  mood?: string;
}): Promise<Activity[]> {
  let query = supabase
    .from('activities')
    .select('title, description, duration, price, link, tags')
    .ilike('city', `%${criteria.city}%`);

  // Filtrage budget (exemple)
  if (criteria.budget === 'petit') query = query.lte('price', 50);
  if (criteria.budget === 'moyen') query = query.gte('price', 50).lte('price', 150);
  if (criteria.budget === 'grand') query = query.gte('price', 150);

  // Filtrage mood (exemple)
  if (criteria.mood) query = query.contains('tags', [criteria.mood]);

  const { data, error } = await query.limit(5);

  if (error) throw new Error(error.message);

  return (data ?? []) as Activity[];
}

// Fonction principale
export async function runActivitySearch(input: string): Promise<Activity[]> {
  const criteria = await TripRequestParser(input);
  return await SupabaseSearchAgent(criteria);
} 
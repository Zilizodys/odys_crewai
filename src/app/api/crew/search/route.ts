import { NextRequest } from 'next/server';
import { runActivitySearch } from '../../../../lib/crew/crew';
import { Activity } from '../../../../types/activity';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const input = body.input;
  if (!input) {
    return new Response(JSON.stringify({ error: 'Champ input requis' }), { status: 400 });
  }
  try {
    const results: Activity[] = await runActivitySearch(input);
    return new Response(JSON.stringify(results), { status: 200 });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
} 
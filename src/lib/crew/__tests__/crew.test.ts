import { TripRequestParser, SupabaseSearchAgent } from '../crew';
import { Activity } from '../../../types/activity';

// Mock du client Supabase
jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => ({
    from: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      ilike: jest.fn().mockReturnThis(),
      lte: jest.fn().mockReturnThis(),
      gte: jest.fn().mockReturnThis(),
      contains: jest.fn().mockReturnThis(),
      limit: jest.fn().mockResolvedValue({
        data: [
          {
            title: 'Balade en barque sur l\'Arno',
            description: 'Profitez d\'une balade romantique sur la rivière Arno à Florence.',
            duration: '2h',
            price: 40,
            link: 'https://exemple.com/activite1',
            tags: ['romantique', 'florence', 'petit budget']
          }
        ],
        error: null
      })
    }))
  }))
}));

describe('CrewAI Tests', () => {
  test('TripRequestParser extrait correctement les critères', async () => {
    const input = 'Je veux un week-end romantique à Florence avec un petit budget';
    const result = await TripRequestParser(input);
    expect(result).toEqual({
      city: 'Florence',
      budget: 'petit',
      mood: 'romantique'
    });
  });

  test('SupabaseSearchAgent retourne des activités', async () => {
    const criteria = {
      city: 'Florence',
      budget: 'petit',
      mood: 'romantique'
    };
    const results = await SupabaseSearchAgent(criteria);
    expect(Array.isArray(results)).toBe(true);
    expect(results.length).toBeLessThanOrEqual(5);
    if (results.length > 0) {
      const activity = results[0];
      expect(activity).toHaveProperty('title');
      expect(activity).toHaveProperty('description');
      expect(activity).toHaveProperty('duration');
      expect(activity).toHaveProperty('price');
      expect(activity).toHaveProperty('link');
      expect(activity).toHaveProperty('tags');
    }
  });
}); 
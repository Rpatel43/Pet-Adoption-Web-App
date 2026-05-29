/**
 * Represents a pet listing fetched from the server.
 */
export interface Pet {
  id: number;
  name: string;
  type: string;
  sex: string;
  bio: string;
  health_info: string;
  size: string;
  weight: string;
  status: string;
  picture: string; // URL to the pet’s image
}

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

/**
 * Fetch all available pet types (for filtering UI).
 *
 * @returns a string array of types, e.g. ['Dog','Cat']
 * @throws Error if the request fails
 */
export async function getPetTypes(): Promise<string[]> {
  const resp = await fetch(`${API_BASE}/pettypes`, {
    credentials: 'include',
  });
  if (!resp.ok) {
    throw new Error('Unable to load pet types');
  }
  const json = await resp.json();
  return json.pet_types as string[];
}

/**
 * Fetch a list of pets, optionally filtered by type.
 *
 * @param type - if provided, filters results to that pet type
 * @returns array of Pet objects
 * @throws Error if the request fails
 */
export async function getPets(type?: string): Promise<Pet[]> {
  // build the URL dynamically to include a query parameter if needed
  const url = new URL(`${API_BASE}/pets`, window.location.origin);
  if (type) {
    url.searchParams.set('type', type);
  }

  const resp = await fetch(url.toString(), {
    credentials: 'include',
  });
  if (!resp.ok) {
    throw new Error('Failed to fetch pet listings');
  }
  const json = await resp.json();
  return json.pets as Pet[];
}

/**
 * Fetch the details for a single pet by its ID.
 *
 * @param id - the numeric pet ID
 * @returns the detailed Pet object
 * @throws Error if the pet is not found or the request fails
 */
export async function getPet(id: number): Promise<Pet> {
  const resp = await fetch(`${API_BASE}/pet/${id}`, {
    credentials: 'include',
  });
  if (!resp.ok) {
    throw new Error(`Pet with ID ${id} not found`);
  }
  const json = await resp.json();
  return json.pet as Pet;
}

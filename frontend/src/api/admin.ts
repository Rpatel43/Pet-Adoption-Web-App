/**
 * All API calls for the admin portal live here.
 * Each function will throw an Error if the HTTP response is not OK.
 */

const ADMIN_BASE = '/api/admin';

/**
 * Shape of the response from a successful admin sign-in.
 */
export interface AdminSession {
  admin: string;  // the username of the signed-in admin
}

/**
 * Data returned by the /dashboard endpoint:
 *  - pet_listings: an array of all pets
 *  - applications: an array of all user applications
 *  - pet_types:   an array of strings for each pet type
 */
export interface AdminDashboardData {
  pet_listings: any[];
  applications: any[];
  pet_types: string[];
}

/**
 * Sign an admin user in.  
 * Sends credentials, and if successful, returns the admin username.
 */
export async function adminSignIn(
  username: string,
  password: string
): Promise<string> {
  const resp = await fetch(`${ADMIN_BASE}/signin`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  if (!resp.ok) {
    const body = await resp.json().catch(() => ({}));
    throw new Error(body.error || 'Unable to sign in as admin');
  }

  const data: AdminSession = await resp.json();
  return data.admin;
}

/**
 * Sign the current admin user out.
 * Clears the server-side session cookie.
 */
export async function adminSignOut(): Promise<void> {
  await fetch(`${ADMIN_BASE}/signout`, {
    method: 'POST',
    credentials: 'include'
  });
}

/**
 * Fetches all the data needed for the admin dashboard:
 * pets, applications, and pet types.
 */
export async function getAdminDashboard(): Promise<AdminDashboardData> {
  const resp = await fetch(`${ADMIN_BASE}/dashboard`, {
    credentials: 'include'
  });
  if (!resp.ok) {
    throw new Error('Failed to load admin dashboard');
  }
  // the JSON comes back as { dashboard: { pet_listings, applications, pet_types } }
  const { dashboard } = await resp.json();
  return dashboard as AdminDashboardData;
}

/**
 * Create a brand-new pet.  
 * Expects a FormData containing all required fields + a picture file.
 * Returns the new pet’s ID.
 */
export async function createPet(form: FormData): Promise<number> {
  const resp = await fetch(`${ADMIN_BASE}/pet`, {
    method: 'POST',
    credentials: 'include',
    body: form
  });

  if (!resp.ok) {
    const body = await resp.json().catch(() => ({}));
    throw new Error(body.error || 'Failed to create pet');
  }

  const result = await resp.json();
  return result.pet_id as number;
}

/**
 * Update an existing pet by ID.  
 * If you pass a FormData, use that; if JSON, serialize accordingly.
 */
export async function updatePet(
  petId: number,
  payload: FormData | Record<string, any>
): Promise<void> {
  const isForm = payload instanceof FormData;
  const resp = await fetch(`${ADMIN_BASE}/pet/${petId}`, {
    method: 'PUT',
    credentials: 'include',
    headers: isForm
      ? undefined
      : { 'Content-Type': 'application/json' },
    body: isForm ? payload : JSON.stringify(payload)
  });

  if (!resp.ok) {
    const body = await resp.json().catch(() => ({}));
    throw new Error(body.error || 'Failed to update pet');
  }
}

/**
 * Delete a pet listing by its ID.
 */
export async function deletePet(petId: number): Promise<void> {
  const resp = await fetch(`${ADMIN_BASE}/pet/${petId}`, {
    method: 'DELETE',
    credentials: 'include'
  });
  if (!resp.ok) {
    throw new Error('Failed to delete pet');
  }
}

/**
 * Change the status of a user’s application.
 */
export async function updateApplicationStatus(
  applicationId: number,
  newStatus: string
): Promise<void> {
  const resp = await fetch(`${ADMIN_BASE}/application/${applicationId}`, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  });
  if (!resp.ok) {
    throw new Error('Failed to update application status');
  }
}

/**
 * Adds a new pet type (e.g. "Rabbit").  
 * Returns the updated list of all pet types.
 */
export async function createPetType(typeName: string): Promise<string[]> {
  const resp = await fetch(`${ADMIN_BASE}/pettypes`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: typeName })
  });

  if (!resp.ok) {
    const body = await resp.json().catch(() => ({}));
    throw new Error(body.error || 'Failed to add pet type');
  }

  const data = await resp.json();
  return data.pet_types as string[];
}

/**
 * Removes an existing pet type by name.  
 * Returns the updated list of pet types.
 */
export async function deletePetType(typeName: string): Promise<string[]> {
  const resp = await fetch(
    `${ADMIN_BASE}/pettypes/${encodeURIComponent(typeName)}`,
    {
      method: 'DELETE',
      credentials: 'include'
    }
  );
  if (!resp.ok) {
    const body = await resp.json().catch(() => ({}));
    throw new Error(body.error || 'Failed to delete pet type');
  }

  const data = await resp.json();
  return data.pet_types as string[];
}

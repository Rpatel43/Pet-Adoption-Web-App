// src/api/applications.ts

/**
 * A user's application to adopt a pet.
 */
export interface Application {
  application_id: number;
  user_id: number;
  pet_id: number;
  status: string;
  application_response: string;
}

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

/**
 * Fetches all of the current user's applications.
 * Sends the session cookie so the server knows who’s asking.
 *
 * @returns an array of Application objects
 * @throws if the request fails
 */
export async function getUserApplications(): Promise<Application[]> {
  const response = await fetch(`${API_BASE}/applications`, {
    credentials: 'include',
  });

  if (!response.ok) {
    // Try to pull an error message from the JSON, else fallback
    const errBody = await response.json().catch(() => ({}));
    throw new Error(errBody.error || 'Unable to load your applications.');
  }

  const data = await response.json();
  return data.applications as Application[];
}

/**
 * Submits a new application for the given pet.
 *
 * @param petId - the ID of the pet to apply for
 * @param applicationResponse - the user's written response
 * @returns the newly created application ID
 * @throws if the request fails
 */
export async function submitApplication(
  petId: number,
  applicationResponse: string
): Promise<number> {
  const response = await fetch(
    `${API_BASE}/pet/${petId}/application`,
    {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ application_response: applicationResponse }),
    }
  );

  if (!response.ok) {
    const errBody = await response.json().catch(() => ({}));
    throw new Error(errBody.error || 'Failed to submit application.');
  }

  const result = await response.json();
  return result.application_id as number;
}

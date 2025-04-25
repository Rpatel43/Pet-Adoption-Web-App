/**
 * API functions for user authentication and session management.
 */

const API_BASE = '/api';

/**
 * Get the current user's session.
 * Returns the username if logged in, or null otherwise.
 */
export async function getSession(): Promise<string | null> {
  const response = await fetch(`${API_BASE}/session`, {
    credentials: 'include',
  });

  if (!response.ok) {
    // If the session endpoint ever returns an error, treat as no session
    return null;
  }

  const data = await response.json();
  // data.user is either null or { id, username }
  return data.user?.username ?? null;
}

/**
 * Sign a user in with username & password.
 * Sets a session cookie on success. Returns the username.
 *
 * @throws Error with message from server on failure.
 */
export async function signIn(
  username: string,
  password: string
): Promise<string> {
  const response = await fetch(`${API_BASE}/signin`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const errBody = await response.json().catch(() => ({}));
    throw new Error(errBody.error || 'Sign in failed');
  }

  const data = await response.json();
  return data.username as string;
}

/**
 * Register a new user.
 * Returns the new username on success.
 *
 * @param firstName - user's first name
 * @param lastName  - user's last name
 * @param username  - desired login handle
 * @param password  - chosen password
 *
 * @throws Error with message from server on failure.
 */
export async function signUp(
  firstName: string,
  lastName: string,
  username: string,
  password: string
): Promise<string> {
  const payload = {
    first_name: firstName,
    last_name: lastName,
    username,
    password,
    password_conf: password, // confirm matches password
  };

  const response = await fetch(`${API_BASE}/signup`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errBody = await response.json().catch(() => ({}));
    throw new Error(errBody.error || 'Sign up failed');
  }

  const data = await response.json();
  return data.username as string;
}

/**
 * Sign the current user out.
 * Clears session on the server.
 */
export async function signOut(): Promise<void> {
  await fetch(`${API_BASE}/signout`, {
    method: 'POST',
    credentials: 'include',
  });
}

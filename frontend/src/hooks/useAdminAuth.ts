import { useContext } from 'react';
import { AuthContext as UserContext } from '../App';

export function useAdminAuth(): boolean {
  const user = useContext(UserContext);
  return Boolean(user);
}

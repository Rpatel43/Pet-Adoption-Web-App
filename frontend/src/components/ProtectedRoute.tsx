/**
 * Wraps any route that requires a signed-in user.
 * If there's no authenticated user in context, redirects to /signin.
 */
interface ProtectedRouteProps {
    children: ReactElement;
  }
  
  const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    // Grab the current user from our AuthContext.
    const user = useContext(AuthContext);
    // Remember where we were trying to go, so we can
    // optionally redirect back after login.
    const location = useLocation();
  
    // If not signed in, send them to the signin page.
    // We pass along `state` so the SignIn page knows
    // where to return afterward (optional).
    if (!user) {
      return (
        <Navigate
          to="/signin"
          replace
          state={{ from: location }}
        />
      );
    }
  
    // If we do have a user, render the protected component.
    return children;
  };
  
  export default ProtectedRoute;
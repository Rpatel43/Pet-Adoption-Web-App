import React, { useState, useEffect, ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { Spinner } from 'react-bootstrap';
import { getAdminDashboard } from '../api/admin';

interface AdminProtectedRouteProps {
  children: ReactNode;
}

const AdminProtectedRoute: React.FC<AdminProtectedRouteProps> = ({ children }) => {
  // tracks whether we're still checking the admin session
  const [isLoading, setIsLoading] = useState(true);
  // tracks if the current user is an authorized admin
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    // Immediately-invoked async function to check admin session
    (async () => {
      try {
        // Attempt to fetch admin-only dashboard data
        await getAdminDashboard();
        setIsAuthorized(true);
      } catch (err) {
        setIsAuthorized(false);
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  // While we’re waiting on the API response, show a spinner
  if (isLoading) {
    return (
      <div className="d-flex justify-content-center my-5">
        <Spinner animation="border" role="status" />
        <span className="visually-hidden">Verifying admin...</span>
      </div>
    );
  }

  // If not an admin, redirect to the admin sign-in page
  if (!isAuthorized) {
    return <Navigate to="/admin/signin" replace />;
  }

  // Otherwise render the protected content
  return <>{children}</>;
};

export default AdminProtectedRoute;

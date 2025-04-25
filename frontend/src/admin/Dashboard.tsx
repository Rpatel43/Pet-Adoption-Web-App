import React, { useState, useEffect } from 'react';
import {
  Tabs,
  Tab,
  Container,
  Spinner,
  Alert,
  Button
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

import AdminProtectedRoute from './AdminProtectedRoute';
import PetManager from './PetManager';
import ApplicationManager from './ApplicationManager';
import PetTypeManager from './PetTypeManager';
import { getAdminDashboard, adminSignOut } from '../api/admin';

const Dashboard: React.FC = () => {
  // Tracks whether we’re waiting for the initial fetch
  const [isLoading, setIsLoading] = useState(true);
  // Holds any error message from fetching
  const [fetchError, setFetchError] = useState<string | null>(null);

  const navigate = useNavigate();

  // Load admin “dashboard” data (to verify session)
  const loadDashboard = async () => {
    setIsLoading(true);
    setFetchError(null);
    try {
      await getAdminDashboard();
    } catch (err: any) {
      setFetchError(err.message || 'Failed to load dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  // On component mount, verify admin session
  useEffect(() => {
    loadDashboard();
  }, []);

  // Handle admin sign-out
  const handleSignOut = async () => {
    await adminSignOut();
    navigate('/admin/signin');
  };

  // Show spinner while we’re verifying
  if (isLoading) {
    return (
      <Container className="text-center my-5">
        <Spinner animation="border" role="status" />
        <p className="mt-3">Loading admin dashboard…</p>
      </Container>
    );
  }

  // Show error if the initial fetch failed
  if (fetchError) {
    return (
      <Container className="my-5">
        <Alert variant="danger">
          {fetchError}
        </Alert>
      </Container>
    );
  }

  // Render the protected dashboard UI
  return (
    <AdminProtectedRoute>
      <Container className="mt-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h2>Admin Dashboard</h2>
          <Button variant="outline-danger" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>

        {/* Tabs for managing pets, applications, and pet types */}
        <Tabs defaultActiveKey="pets" className="mb-3">
          <Tab eventKey="pets" title="Pets">
            <PetManager />
          </Tab>
          <Tab eventKey="applications" title="Applications">
            <ApplicationManager />
          </Tab>
          <Tab eventKey="types" title="Pet Types">
            <PetTypeManager />
          </Tab>
        </Tabs>
      </Container>
    </AdminProtectedRoute>
  );
};

export default Dashboard;

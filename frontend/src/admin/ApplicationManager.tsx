import React, { useState, useEffect } from 'react';
import { Table, Form, Spinner, Alert, Container } from 'react-bootstrap';
import { getAdminDashboard, updateApplicationStatus } from '../api/admin';

// Define the shape of an application record
interface Application {
  application_id: number;
  user_id: number;
  pet_id: number;
  status: string;
  application_response: string;
}

const ApplicationManager: React.FC = () => {
  // Holds the list of applications
  const [applications, setApplications] = useState<Application[]>([]);
  // Loading and error states
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  // Fetch the dashboard data (which includes applications) from the API
  const loadApplications = async () => {
    setIsLoading(true);
    setFetchError(null);

    try {
      const data = await getAdminDashboard();
      // The API returns a shape like { applications: [...] }
      setApplications(data.applications as Application[]);
    } catch (err: any) {
      setFetchError(err.message || 'Failed to load applications');
    } finally {
      setIsLoading(false);
    }
  };

  // On mount, load the applications
  useEffect(() => {
    loadApplications();
  }, []);

  // Handle status changes: call API then refresh list
  const handleStatusChange = async (appId: number, newStatus: string) => {
    try {
      await updateApplicationStatus(appId, newStatus);
      // After updating, re-fetch the list to reflect the change
      loadApplications();
    } catch (err: any) {
      // In a real app you might show a toast or inline error here
      console.error(`Error updating status for ${appId}:`, err);
    }
  };

  // Show spinner while loading
  if (isLoading) {
    return (
      <Container className="text-center my-5">
        <Spinner animation="border" role="status" />
        <p className="mt-3">Loading applications…</p>
      </Container>
    );
  }

  // Show error if fetch failed
  if (fetchError) {
    return (
      <Container className="my-5">
        <Alert variant="danger">
          {fetchError}
        </Alert>
      </Container>
    );
  }

  // Render the applications table
  return (
    <Container className="my-4">
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Application ID</th>
            <th>User ID</th>
            <th>Pet ID</th>
            <th>Status</th>
            <th>Your Response</th>
          </tr>
        </thead>
        <tbody>
          {applications.map(app => (
            <tr key={app.application_id}>
              <td>{app.application_id}</td>
              <td>{app.user_id}</td>
              <td>{app.pet_id}</td>
              <td>
                <Form.Select
                  size="sm"
                  value={app.status}
                  onChange={e => handleStatusChange(app.application_id, e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="denied">Denied</option>
                </Form.Select>
              </td>
              <td>{app.application_response}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      {applications.length === 0 && (
        <p className="text-center">No applications have been submitted yet.</p>
      )}
    </Container>
  );
};

export default ApplicationManager;

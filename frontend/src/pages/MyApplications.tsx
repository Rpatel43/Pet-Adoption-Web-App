import React, { useState, useEffect } from 'react';
import { Table, Container, Spinner, Alert } from 'react-bootstrap';
import { getUserApplications, Application } from '../api/applications';

/**
 * Page that displays all applications submitted by the current user.
 */
const MyApplications: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch the user's applications on mount
  useEffect(() => {
    async function loadApplications() {
      setIsLoading(true);
      setError(null);
      try {
        const apps = await getUserApplications();
        setApplications(apps);
      } catch (err: any) {
        console.error('Failed to load applications:', err);
        setError(err.message || 'Could not fetch your applications.');
      } finally {
        setIsLoading(false);
      }
    }

    loadApplications();
  }, []);

  // Show spinner while loading
  if (isLoading) {
    return (
      <Container className="my-5 text-center">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Loading your applications…</span>
      </Container>
    );
  }

  // Show error alert on failure
  if (error) {
    return (
      <Container className="my-5">
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  // Inform the user if they have no applications
  if (applications.length === 0) {
    return (
      <Container className="my-5">
        <Alert variant="info">You have not submitted any applications yet.</Alert>
      </Container>
    );
  }

  // Render the applications table
  return (
    <Container className="my-4">
      <h2 className="mb-3">My Applications</h2>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Application ID</th>
            <th>Pet ID</th>
            <th>Status</th>
            <th>Your Response</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app.application_id}>
              <td>{app.application_id}</td>
              <td>{app.pet_id}</td>
              <td>{app.status}</td>
              <td>{app.application_response}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default MyApplications;

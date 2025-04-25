import React, { useState } from 'react';
import { Form, Button, Card, Alert, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { adminSignIn } from '../api/admin';

const AdminSignIn: React.FC = () => {
  // Controlled form fields
  const [adminUsername, setAdminUsername] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  // Error message (if sign-in fails)
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  // Submission state to disable button and show spinner
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  // Called when the form is submitted
  const handleSignIn = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMessage(null);    // clear any existing error
    setIsSubmitting(true);

    try {
      // Attempt to sign in via API
      await adminSignIn(adminUsername, adminPassword);
      toast.success('Successfully signed in as admin!');
      // On success, redirect to the dashboard
      navigate('/admin/dashboard');
    } catch (err: any) {
      // Display backend error or fallback message
      setErrorMessage(err.message || 'Sign in failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ minHeight: '80vh' }}
    >
      <Card style={{ width: '100%', maxWidth: '380px' }}>
        <Card.Body>
          <Card.Title className="text-center mb-4">
            Admin Sign In
          </Card.Title>

          {/* Show error if one exists */}
          {errorMessage && (
            <Alert
              variant="danger"
              onClose={() => setErrorMessage(null)}
              dismissible
            >
              {errorMessage}
            </Alert>
          )}

          <Form onSubmit={handleSignIn}>
            <Form.Group controlId="adminUsername" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter admin username"
                value={adminUsername}
                onChange={e => setAdminUsername(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="adminPassword" className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter your password"
                value={adminPassword}
                onChange={e => setAdminPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Button
              variant="primary"
              type="submit"
              className="w-100"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Spinner
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                  <span className="ms-2">Signing in…</span>
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default AdminSignIn;

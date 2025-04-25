import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { submitApplication } from '../api/applications';

/**
 * Page for submitting a new application to adopt a pet.
 * Requires the user to be signed in (wrapped by ProtectedRoute).
 */
const ApplyForm: React.FC = () => {
  // ─── Route Params & Navigation ─────────────────────────────────────────────
  const { id } = useParams<{ id: string }>();
  const petId = Number(id);
  const navigate = useNavigate();

  // ─── Component State ────────────────────────────────────────────────────────
  // The user's typed message
  const [message, setMessage] = useState('');
  // Error message for form validation or API errors
  const [error, setError] = useState<string | null>(null);
  // Loading spinner when submitting
  const [isSubmitting, setIsSubmitting] = useState(false);

  // ─── Form Submission Handler ────────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Basic validation
    if (!message.trim()) {
      setError('Please enter your application message.');
      return;
    }
    setError(null);
    setIsSubmitting(true);

    try {
      // Call the API to submit the application
      const appId = await submitApplication(petId, message.trim());
      toast.success(`Application #${appId} submitted!`);
      // Redirect to home or applications list
      navigate('/');
    } catch (err: any) {
      // Display any server-side errors
      setError(err.message || 'Failed to submit application.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // ─── Render ─────────────────────────────────────────────────────────────────
  return (
    <Card className="mx-auto my-5" style={{ maxWidth: '600px' }}>
      <Card.Body>
        <Card.Title className="mb-4">Apply for Pet #{petId}</Card.Title>

        {error && (
          <Alert variant="danger" onClose={() => setError(null)} dismissible>
            {error}
          </Alert>
        )}

        <Form onSubmit={handleSubmit} noValidate>
          <Form.Group controlId="applicationMessage" className="mb-3">
            <Form.Label>Your Application Message</Form.Label>
            <Form.Control
              as="textarea"
              rows={5}
              placeholder="Tell us why you'd make a great owner..."
              value={message}
              onChange={e => setMessage(e.target.value)}
              isInvalid={!!error}
              disabled={isSubmitting}
              required
            />
            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </Form.Group>

          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />{' '}
                Submitting...
              </>
            ) : (
              'Submit Application'
            )}
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default ApplyForm;

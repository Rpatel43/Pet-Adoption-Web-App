import React, { useState } from 'react';
import { Card, Form, Button, Alert, Spinner, Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { signIn } from '../api/auth';

interface SignInProps {
  /** 
   * Called when sign-in succeeds, passing back the
   * signed-in user info ({ username }).
   */
  onLogin: (user: { username: string }) => void;
}

/**
 * SignIn page component.
 * Validates inputs, calls API, and notifies parent on success.
 */
const SignIn: React.FC<SignInProps> = ({ onLogin }) => {
  // ─── Local state ─────────────────────────────────────────────────────────
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const navigate = useNavigate();

  // ─── Form submission handler ─────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Reset previous errors
    setFieldErrors({});
    setSubmitError(null);

    // Basic client-side validation
    const errors: Record<string, string> = {};
    if (!username.trim()) errors.username = 'Username is required';
    if (!password) errors.password = 'Password is required';

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setIsSubmitting(true);
    try {
      // Call API to authenticate
      const user = await signIn(username.trim(), password);
      // Notify parent component
      onLogin({ username: user });
      toast.success('Successfully signed in!');
      // Redirect to home page
      navigate('/');
    } catch (err: any) {
      // Show error from server (or generic)
      setSubmitError(err.message || 'Sign in failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <Container className="d-flex justify-content-center my-5">
      <Card style={{ maxWidth: '400px', width: '100%' }}>
        <Card.Body>
          <Card.Title className="mb-4 text-center">Sign In</Card.Title>

          {submitError && (
            <Alert
              variant="danger"
              onClose={() => setSubmitError(null)}
              dismissible
            >
              {submitError}
            </Alert>
          )}

          <Form noValidate onSubmit={handleSubmit}>
            {/* Username Field */}
            <Form.Group controlId="signinUsername" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                isInvalid={!!fieldErrors.username}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.username}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Password Field */}
            <Form.Group controlId="signinPassword" className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                isInvalid={!!fieldErrors.password}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.password}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              className="w-100"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />{' '}
                  Signing In…
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default SignIn;

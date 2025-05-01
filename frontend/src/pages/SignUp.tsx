import React, { useState } from 'react';
import {
  Card,
  Form,
  Button,
  Alert,
  Spinner,
  Container
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { signUp, signIn } from '../api/auth';

interface SignUpProps {
  /**
   * Called when sign-up succeeds;
   * parent will receive the new user ({ username }).
   */
  onSignup: (user: { username: string }) => void;
}

/**
 * SignUp page component.
 * Handles input validation, signup API call, and navigation on success.
 */
const SignUp: React.FC<SignUpProps> = ({ onSignup }) => {
  // ─── Local State ─────────────────────────────────────────────────────────
  const [firstName, setFirstName]     = useState<string>('');
  const [lastName, setLastName]       = useState<string>('');
  const [username, setUsername]       = useState<string>('');
  const [password, setPassword]       = useState<string>('');
  const [passwordConf, setPasswordConf] = useState<string>('');

  // Field-specific validation errors
  const [fieldErrors, setFieldErrors] = useState<Record<string,string>>({});
  // Generic submit error from server
  const [submitError, setSubmitError] = useState<string | null>(null);
  // Loading spinner on submit
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const navigate = useNavigate();

  // ─── Form Submit Handler ─────────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});
    setSubmitError(null);

    // Simple client-side validation
    const errors: Record<string,string> = {};
    if (!firstName.trim())    errors.firstName = 'First name is required';
    if (!lastName.trim())     errors.lastName  = 'Last name is required';
    if (username.trim().length < 3)
      errors.username = 'Username must be at least 3 characters';
    if (password.length < 8)
      errors.password = 'Password must be at least 8 characters';
    if (password !== passwordConf)
      errors.passwordConf = 'Passwords do not match';

    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      return;
    }

    setIsSubmitting(true);
    try {
      // Call API to create account
      const newUsername = await signUp(
        firstName.trim(),
        lastName.trim(),
        username.trim(),
        password
      );
      // now have user sign in
      await signIn(newUsername, password)
      onSignup({ username: newUsername });
      toast.success('Account created successfully!');
      // Redirect to home (or anywhere)
      navigate('/');
    } catch (err: any) {
      // Show server-side error
      setSubmitError(err.message || 'Sign up failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <Container className="d-flex justify-content-center my-5">
      <Card style={{ maxWidth: '400px', width: '100%' }}>
        <Card.Body>
          <Card.Title className="mb-4 text-center">Sign Up</Card.Title>

          {submitError && (
            <Alert
              variant="danger"
              dismissible
              onClose={() => setSubmitError(null)}
            >
              {submitError}
            </Alert>
          )}

          <Form noValidate onSubmit={handleSubmit}>
            {/* First Name */}
            <Form.Group controlId="signUpFirstName" className="mb-3">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter your first name"
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                isInvalid={!!fieldErrors.firstName}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.firstName}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Last Name */}
            <Form.Group controlId="signUpLastName" className="mb-3">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter your last name"
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                isInvalid={!!fieldErrors.lastName}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.lastName}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Username */}
            <Form.Group controlId="signUpUsername" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Choose a username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                isInvalid={!!fieldErrors.username}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.username}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Password */}
            <Form.Group controlId="signUpPassword" className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Create a password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                isInvalid={!!fieldErrors.password}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.password}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Confirm Password */}
            <Form.Group controlId="signUpPasswordConf" className="mb-4">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Re-enter your password"
                value={passwordConf}
                onChange={e => setPasswordConf(e.target.value)}
                isInvalid={!!fieldErrors.passwordConf}
                disabled={isSubmitting}
              />
              <Form.Control.Feedback type="invalid">
                {fieldErrors.passwordConf}
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
                  Creating Account…
                </>
              ) : (
                'Sign Up'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default SignUp;

import React, { useContext } from 'react';
import { Card, Button, Container, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { AuthContext } from '../App';

/**
 * Home page component.
 * Shows a welcome message and navigation buttons
 * depending on whether the user is signed in.
 */
const Home: React.FC = () => {
  // Pull the current user (or null) from context
  const user = useContext(AuthContext);

  return (
    <Container className="d-flex justify-content-center align-items-center mt-5">
      <Card style={{ maxWidth: '500px', width: '100%' }} className="text-center p-4">
        <Card.Title as="h1">Welcome to PetAdopt</Card.Title>

        {user ? (
          // If we're signed in, greet them and show application/listings links
          <>
            <Card.Text className="my-3">Hello, <strong>{user.username}</strong>!</Card.Text>
            <div className="d-flex justify-content-center gap-2">
              <Button as={Link} to="/applications" variant="primary">
                My Applications
              </Button>
              <Button as={Link} to="/listings" variant="outline-primary">
                Browse Listings
              </Button>
            </div>
          </>
        ) : (
          // Not signed in: prompt to sign in or sign up
          <>
            <Card.Text className="my-3">
              Please sign in or sign up to get started.
            </Card.Text>
            <div className="d-flex justify-content-center gap-2">
              <Button as={Link} to="/signin" variant="primary">
                Sign In
              </Button>
              <Button as={Link} to="/signup" variant="outline-primary">
                Sign Up
              </Button>
            </div>
          </>
        )}
      </Card>
    </Container>
  );
};

export default Home;

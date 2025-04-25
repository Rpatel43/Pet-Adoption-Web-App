import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spinner, Alert, Container } from 'react-bootstrap';
import { getPet, Pet } from '../api/pets';

/**
 * Page to show all details for a single pet.
 * Includes a button to apply, which requires the user be signed in.
 */
const PetDetail: React.FC = () => {
  // ─── Route & Navigation Hooks ─────────────────────────────────────────────
  const { id } = useParams<{ id: string }>();
  const petId = Number(id);
  const navigate = useNavigate();

  // ─── Local State ──────────────────────────────────────────────────────────
  // The fetched pet object (or null if not found)
  const [pet, setPet] = useState<Pet | null>(null);
  // Loading & error indicators
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // ─── Fetch Pet Data ───────────────────────────────────────────────────────
  useEffect(() => {
    // Guard against invalid ID
    if (!petId) {
      setError('Invalid pet ID.');
      setIsLoading(false);
      return;
    }

    // Retrieve the pet details
    getPet(petId)
      .then(fetched => setPet(fetched))
      .catch(err => {
        console.error('Error fetching pet details:', err);
        setError('Could not load pet details.');
      })
      .finally(() => setIsLoading(false));
  }, [petId]);

  // ─── Render States ────────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <Container className="d-flex justify-content-center my-5">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Loading pet details…</span>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="my-5">
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  if (!pet) {
    return (
      <Container className="my-5">
        <Alert variant="warning">Pet not found.</Alert>
      </Container>
    );
  }

  // ─── Main Detail Card ────────────────────────────────────────────────────
  return (
    <Container className="my-5 d-flex justify-content-center">
      <Card style={{ width: '100%', maxWidth: '600px' }}>
        {/* Pet image */}
        <Card.Img
          variant="top"
          src={pet.picture}
          alt={`Photo of ${pet.name}`}
          onError={(e) => { e.currentTarget.src = '/default-pet.png'; }}
        />

        <Card.Body>
          <Card.Title as="h2" className="mb-3">
            {pet.name}
          </Card.Title>

          {/* Pet details list */}
          <ul className="list-unstyled mb-4">
            <li><strong>Type:</strong> {pet.type}</li>
            <li><strong>Sex:</strong> {pet.sex}</li>
            <li><strong>Bio:</strong> {pet.bio}</li>
            <li><strong>Health Info:</strong> {pet.health_info}</li>
            <li><strong>Size:</strong> {pet.size}</li>
            <li><strong>Weight:</strong> {pet.weight}</li>
            <li><strong>Status:</strong> {pet.status}</li>
          </ul>

          {/* Apply button */}
          <Button
            variant="primary"
            onClick={() => navigate(`/apply/${pet.id}`)}
          >
            Apply for this Pet
          </Button>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default PetDetail;

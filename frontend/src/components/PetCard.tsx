import React from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import type { Pet } from '../api/pets';

interface PetCardProps {
  pet: Pet;
}

/**
 * A simple card to display a pet's picture and name.
 * Clicking anywhere on the card takes you to the pet's detail page.
 */
const PetCard: React.FC<PetCardProps> = ({ pet }) => {
  // Fallback image if the src fails
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src = '/default-pet.png';
  };

  return (
    <Card className="h-100" style={{ cursor: 'pointer' }}>
      <Link to={`/pets/${pet.id}`} style={{ color: 'inherit', textDecoration: 'none' }}>
        {/* Pet picture */}
        <Card.Img
          variant="top"
          src={pet.picture}
          alt={`Photo of ${pet.name}`}
          onError={handleImageError}
        />

        {/* Pet name */}
        <Card.Body className="text-center">
          <Card.Title>{pet.name}</Card.Title>
        </Card.Body>
      </Link>
    </Card>
  );
};

export default PetCard;
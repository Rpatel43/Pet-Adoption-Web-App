import React, { useState, useEffect } from 'react';
import { Row, Col, Form, Spinner, Alert, Container } from 'react-bootstrap';
import type { Pet } from '../api/pets';
import { getPetTypes, getPets } from '../api/pets';
import PetCard from '../components/PetCard';
import Pagination from '../components/Pagination';

const ITEMS_PER_PAGE = 6;

const Listings: React.FC = () => {
  // ─── State ───────────────────────────────────────────────────────────────
  // All pet types for the filter dropdown
  const [petTypes, setPetTypes] = useState<string[]>([]);
  // Currently selected filter (empty = no filter)
  const [selectedType, setSelectedType] = useState<string>('');
  // Full list of pets returned from the API
  const [allPets, setAllPets] = useState<Pet[]>([]);
  // Loading & error states
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  // Pagination: current page index (1-based)
  const [currentPage, setCurrentPage] = useState<number>(1);

  // ─── Fetch Pet Types ─────────────────────────────────────────────────────
  useEffect(() => {
    getPetTypes()
      .then(types => setPetTypes(types))
      .catch(err => {
        console.error('Failed to load pet types:', err);
        setLoadError('Could not load pet types.');
      });
  }, []);

  // ─── Fetch Pets (with Filter) ─────────────────────────────────────────────
  useEffect(() => {
    setIsLoading(true);
    setLoadError(null);

    getPets(selectedType)
      .then(pets => {
        setAllPets(pets);
        setCurrentPage(1); // reset to first page on filter change
      })
      .catch(err => {
        console.error('Failed to load pets:', err);
        setLoadError('Could not load pet listings.');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [selectedType]);

  // ─── Compute Pagination ───────────────────────────────────────────────────
  const totalPages = Math.max(1, Math.ceil(allPets.length / ITEMS_PER_PAGE));
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const visiblePets = allPets.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  // ─── Render ───────────────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Loading pets…</span>
      </div>
    );
  }

  if (loadError) {
    return (
      <Container className="my-5">
        <Alert variant="danger">{loadError}</Alert>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      {/* Filter Dropdown */}
      <Form.Select
        value={selectedType}
        onChange={e => setSelectedType(e.target.value)}
        className="mb-4"
        aria-label="Filter by pet type"
      >
        <option value="">All Types</option>
        {petTypes.map(type => (
          <option key={type} value={type}>
            {type}
          </option>
        ))}
      </Form.Select>

      {/* Pet Cards Grid */}
      <Row xs={1} sm={2} md={3} lg={3} className="g-4">
        {visiblePets.map(pet => (
          <Col key={pet.id}>
            <PetCard pet={pet} />
          </Col>
        ))}
        {visiblePets.length === 0 && (
          <Col>
            <Alert variant="info">No pets found for this filter.</Alert>
          </Col>
        )}
      </Row>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-center mt-4">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={page => setCurrentPage(page)}
          />
        </div>
      )}
    </Container>
  );
};

export default Listings;

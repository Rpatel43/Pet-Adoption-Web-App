import React, { useState, useEffect, FormEvent } from 'react';
import {
  Container,
  Form,
  Button,
  ListGroup,
  Spinner,
  Alert,
  Row,
  Col
} from 'react-bootstrap';
import {
  getAdminDashboard,
  createPetType,
  deletePetType
} from '../api/admin';

const PetTypeManager: React.FC = () => {
  // ─── State ───────────────────────────────────────────────────────────────
  // The list of current pet types
  const [petTypes, setPetTypes] = useState<string[]>([]);
  // Text input for a new type name
  const [newTypeName, setNewTypeName] = useState('');
  // Loading & error states for fetching the list
  const [isLoading, setIsLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  // State for the “add type” form
  const [isAdding, setIsAdding] = useState(false);
  const [formError, setFormError] = useState<string>('');

  // ─── Data Loading ────────────────────────────────────────────────────────
  const loadPetTypes = async () => {
    setIsLoading(true);
    setFetchError(null);
    try {
      const data = await getAdminDashboard();
      setPetTypes(data.pet_types);
    } catch (err: any) {
      setFetchError(err.message || 'Failed to load pet types');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadPetTypes();
  }, []);

  // ─── Handlers ─────────────────────────────────────────────────────────────
  const handleAddType = async (e: FormEvent) => {
    e.preventDefault();
    if (!newTypeName.trim()) {
      setFormError('Type name cannot be empty');
      return;
    }
    setFormError('');
    setIsAdding(true);

    try {
      const updatedTypes = await createPetType(newTypeName.trim());
      setPetTypes(updatedTypes);
      setNewTypeName('');
    } catch (err: any) {
      // show any API error
      setFormError(err.message || 'Could not add pet type');
    } finally {
      setIsAdding(false);
    }
  };

  const handleDeleteType = async (typeToDelete: string) => {
    try {
      await deletePetType(typeToDelete);
      // refresh after deletion
      loadPetTypes();
    } catch (err: any) {
      // for simplicity, reuse fetchError
      setFetchError(err.message || `Failed to delete "${typeToDelete}"`);
    }
  };

  // ─── Render Loading / Error ───────────────────────────────────────────────
  if (isLoading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Loading pet types…</span>
      </div>
    );
  }

  if (fetchError) {
    return (
      <Container className="my-5">
        <Alert variant="danger">{fetchError}</Alert>
      </Container>
    );
  }

  // ─── Main Render ──────────────────────────────────────────────────────────
  return (
    <Container className="my-4">
      <h3 className="mb-3">Manage Pet Types</h3>

      {/* Add new type form */}
      <Form onSubmit={handleAddType} className="mb-4">
        <Row className="g-2 align-items-center">
          <Col xs="auto">
            <Form.Control
              type="text"
              placeholder="New pet type"
              value={newTypeName}
              onChange={e => setNewTypeName(e.target.value)}
              isInvalid={!!formError}
              disabled={isAdding}
            />
            <Form.Control.Feedback type="invalid">
              {formError}
            </Form.Control.Feedback>
          </Col>
          <Col xs="auto">
            <Button type="submit" disabled={isAdding}>
              {isAdding ? (
                <Spinner animation="border" size="sm" role="status" />
              ) : (
                'Add Type'
              )}
            </Button>
          </Col>
        </Row>
      </Form>

      {/* Current pet types list */}
      <ListGroup>
        {petTypes.map(type => (
          <ListGroup.Item
            key={type}
            className="d-flex justify-content-between align-items-center"
          >
            {type}
            <Button
              variant="outline-danger"
              size="sm"
              onClick={() => handleDeleteType(type)}
            >
              Delete
            </Button>
          </ListGroup.Item>
        ))}
        {petTypes.length === 0 && (
          <ListGroup.Item>No pet types found.</ListGroup.Item>
        )}
      </ListGroup>
    </Container>
  );
};

export default PetTypeManager;

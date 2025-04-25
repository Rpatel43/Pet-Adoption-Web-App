// @ts-nocheck
import React, { useState, useEffect } from 'react';
import {
  Container,
  Table,
  Button,
  Modal,
  Form,
  Alert,
  Spinner
} from 'react-bootstrap';
import {
  getAdminDashboard,
  createPet,
  updatePet,
  deletePet
} from '../api/admin';

interface Pet {
  id: number;
  name: string;
  type: string;
  sex: string;
  bio: string;
  health_info: string;
  size: string;
  weight: string;
  status: string;
  picture: string;
}

const PetManager: React.FC = () => {
  // Main data & UI state
  const [pets, setPets] = useState<Pet[]>([]);
  const [petTypes, setPetTypes] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  // Modal & form state
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentPet, setCurrentPet] = useState<Pet | null>(null);
  const [formData, setFormData] = useState<{
    name: string;
    type: string;
    sex: string;
    bio: string;
    health_info: string;
    size: string;
    weight: string;
    status: string;
    pictureFile: File | null;
  }>({
    name: '',
    type: '',
    sex: '',
    bio: '',
    health_info: '',
    size: '',
    weight: '',
    status: '',
    pictureFile: null
  });
  const [formErrors, setFormErrors] = useState<Record<string,string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Delete confirmation state
  const [deletePetId, setDeletePetId] = useState<number | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Fetch dashboard data (pets + types)
  const loadData = async () => {
    setIsLoading(true);
    setFetchError(null);
    try {
      const data = await getAdminDashboard();
      setPets(data.pet_listings as Pet[]);
      setPetTypes(data.pet_types);
    } catch (err: any) {
      setFetchError(err.message || 'Failed to load pet data');
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadData();
  }, []);

  // Open “Add Pet” modal
  const handleAddClick = () => {
    setIsEditing(false);
    setCurrentPet(null);
    setFormData({
      name: '',
      type: '',
      sex: '',
      bio: '',
      health_info: '',
      size: '',
      weight: '',
      status: '',
      pictureFile: null
    });
    setFormErrors({});
    setShowModal(true);
  };

  // Open “Edit Pet” modal
  const handleEditClick = (pet: Pet) => {
    setIsEditing(true);
    setCurrentPet(pet);
    setFormData({
      name: pet.name,
      type: pet.type,
      sex: pet.sex,
      bio: pet.bio,
      health_info: pet.health_info,
      size: pet.size,
      weight: pet.weight,
      status: pet.status,
      pictureFile: null
    });
    setFormErrors({});
    setShowModal(true);
  };

  // Open delete confirmation
  const handleDeleteClick = (id: number) => {
    setDeletePetId(id);
    setShowDeleteConfirm(true);
  };

  // Perform deletion
  const confirmDelete = async () => {
    if (deletePetId == null) return;
    try {
      await deletePet(deletePetId);
      setShowDeleteConfirm(false);
      setDeletePetId(null);
      loadData();
    } catch (err: any) {
      setFetchError(err.message || 'Delete failed');
    }
  };

  // Basic form validation
  const validateForm = () => {
    const errors: Record<string,string> = {};
    if (!formData.name.trim()) errors.name = 'Name is required';
    if (!formData.type) errors.type = 'Type is required';
    if (!formData.sex) errors.sex = 'Sex is required';
    if (!formData.size.trim()) errors.size = 'Size is required';
    if (!formData.weight.trim()) errors.weight = 'Weight is required';
    if (!formData.status) errors.status = 'Status is required';
    if (!formData.bio.trim()) errors.bio = 'Bio is required';
    if (!formData.health_info.trim()) errors.health_info = 'Health info is required';
    if (!isEditing && !formData.pictureFile) errors.pictureFile = 'Picture is required';
    return errors;
  };

  // Submit add/edit form
  const handleFormSubmit = async () => {
    const errors = validateForm();
    setFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setIsSubmitting(true);

    const payload = new FormData();
    payload.append('name', formData.name);
    payload.append('type', formData.type);
    payload.append('sex', formData.sex);
    payload.append('bio', formData.bio);
    payload.append('health_info', formData.health_info);
    payload.append('size', formData.size);
    payload.append('weight', formData.weight);
    payload.append('status', formData.status);
    if (formData.pictureFile) {
      payload.append('picture', formData.pictureFile);
    }

    try {
      if (isEditing && currentPet) {
        await updatePet(currentPet.id, payload);
      } else {
        await createPet(payload);
      }
      setShowModal(false);
      loadData();
    } catch (err: any) {
      setFetchError(err.message || 'Save failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Render loading or error
  if (isLoading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status" />
      </div>
    );
  }
  if (fetchError) {
    return <Alert variant="danger">{fetchError}</Alert>;
  }

  // Main render
  return (
    <Container className="my-4">
      <Button variant="success" onClick={handleAddClick} className="mb-3">
        Add New Pet
      </Button>

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {pets.map(pet => (
            <tr key={pet.id}>
              <td>{pet.id}</td>
              <td>{pet.name}</td>
              <td>{pet.type}</td>
              <td>{pet.status}</td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  onClick={() => handleEditClick(pet)}
                  className="me-2"
                >
                  Edit
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDeleteClick(pet.id)}
                >
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Add / Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{isEditing ? 'Edit Pet' : 'Add Pet'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            {/* Name */}
            <Form.Group controlId="petName" className="mb-3">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter pet name"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
                isInvalid={!!formErrors.name}
              />
              <Form.Control.Feedback type="invalid">
                {formErrors.name}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Type */}
            <Form.Group controlId="petType" className="mb-3">
              <Form.Label>Type</Form.Label>
              <Form.Select
                value={formData.type}
                onChange={e => setFormData({ ...formData, type: e.target.value })}
                isInvalid={!!formErrors.type}
              >
                <option value="">Choose a type</option>
                {petTypes.map(t => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </Form.Select>
              <Form.Control.Feedback type="invalid">
                {formErrors.type}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Sex */}
            <Form.Group controlId="petSex" className="mb-3">
              <Form.Label>Sex</Form.Label>
              <Form.Select
                value={formData.sex}
                onChange={e => setFormData({ ...formData, sex: e.target.value })}
                isInvalid={!!formErrors.sex}
              >
                <option value="">Choose sex</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
              </Form.Select>
              <Form.Control.Feedback type="invalid">
                {formErrors.sex}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Size */}
            <Form.Group controlId="petSize" className="mb-3">
              <Form.Label>Size</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter size (e.g., Small, Medium)"
                value={formData.size}
                onChange={e => setFormData({ ...formData, size: e.target.value })}
                isInvalid={!!formErrors.size}
              />
              <Form.Control.Feedback type="invalid">
                {formErrors.size}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Weight */}
            <Form.Group controlId="petWeight" className="mb-3">
              <Form.Label>Weight</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter weight (e.g., 10 lbs)"
                value={formData.weight}
                onChange={e => setFormData({ ...formData, weight: e.target.value })}
                isInvalid={!!formErrors.weight}
              />
              <Form.Control.Feedback type="invalid">
                {formErrors.weight}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Status */}
            <Form.Group controlId="petStatus" className="mb-3">
              <Form.Label>Status</Form.Label>
              <Form.Select
                value={formData.status}
                onChange={e => setFormData({ ...formData, status: e.target.value })}
                isInvalid={!!formErrors.status}
              >
                <option value="">Choose status</option>
                <option value="Available">Available</option>
                <option value="Pending">Pending</option>
                <option value="Adopted">Adopted</option>
              </Form.Select>
              <Form.Control.Feedback type="invalid">
                {formErrors.status}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Bio */}
            <Form.Group controlId="petBio" className="mb-3">
              <Form.Label>Bio</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="Short bio for the pet"
                value={formData.bio}
                onChange={e => setFormData({ ...formData, bio: e.target.value })}
                isInvalid={!!formErrors.bio}
              />
              <Form.Control.Feedback type="invalid">
                {formErrors.bio}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Health Info */}
            <Form.Group controlId="petHealthInfo" className="mb-3">
              <Form.Label>Health Info</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                placeholder="Health details"
                value={formData.health_info}
                onChange={e => setFormData({ ...formData, health_info: e.target.value })}
                isInvalid={!!formErrors.health_info}
              />
              <Form.Control.Feedback type="invalid">
                {formErrors.health_info}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Picture */}
            {!isEditing && (
              <Form.Group controlId="petPicture" className="mb-3">
                <Form.Label>Picture</Form.Label>
                <Form.Control
                  type="file"
                  accept="image/*"
                  onChange={e => {
                    const file = e.target.files?.[0] || null;
                    setFormData({ ...formData, pictureFile: file });
                  }}
                  isInvalid={!!formErrors.pictureFile}
                />
                <Form.Control.Feedback type="invalid">
                  {formErrors.pictureFile}
                </Form.Control.Feedback>
              </Form.Group>
            )}
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setShowModal(false)}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleFormSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <Spinner animation="border" size="sm" />
            ) : isEditing ? 'Save Changes' : 'Create Pet'}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Delete Confirmation */}
      <Modal
        show={showDeleteConfirm}
        onHide={() => setShowDeleteConfirm(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete this pet listing?
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setShowDeleteConfirm(false)}
          >
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default PetManager;

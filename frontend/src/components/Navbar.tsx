import React, { useContext } from 'react';
import { Navbar as BsNav, Nav, Container, Button } from 'react-bootstrap';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext, AdminContext } from '../App';
import { signOut } from '../api/auth';
import { adminSignOut } from '../api/admin';

// Main navigation bar that adapts for both regular users and admins.
const Navbar: React.FC = () => {
  const user = useContext(AuthContext);
  const admin = useContext(AdminContext);
  const navigate = useNavigate();
  const location = useLocation();

  // Handle user logout
  const handleUserSignOut = async () => {
    try {
      await signOut();
      // Reload page to clear any stale context or cookies
      window.location.reload();
    } catch (err) {
      console.error('Error signing out user:', err);
    }
  };

  // Handle admin logout
  const handleAdminSignOut = async () => {
    try {
      await adminSignOut();
      navigate('/admin/signin');
      window.location.reload();
    } catch (err) {
      console.error('Error signing out admin:', err);
    }
  };

  // Decide where the brand logo should link
  const brandLink = admin ? '/admin/dashboard' : '/';

  return (
    <BsNav bg="light" expand="lg">
      <Container>
        <BsNav.Brand as={Link} to={brandLink}>
          PetAdopt
        </BsNav.Brand>
        <BsNav.Toggle aria-controls="main-navbar" />
        <BsNav.Collapse id="main-navbar">
          {/* Left side links: only for non-admin users */}
          <Nav className="me-auto">
            {!admin && (
              <>
                <Nav.Link as={Link} to="/listings">Listings</Nav.Link>
                {user && (
                  <Nav.Link as={Link} to="/applications">My Applications</Nav.Link>
                )}
              </>
            )}
          </Nav>

          {/* Right side: sign in / sign out / user greeting */}
          <Nav>
            {admin ? (
              <>
                <span className="navbar-text me-3">Admin: {admin.admin}</span>
                <Button variant="outline-danger" onClick={handleAdminSignOut}>
                  Sign Out
                </Button>
              </>
            ) : user ? (
              <>
                <span className="navbar-text me-3">Hello, {user.username}</span>
                <Button variant="outline-danger" onClick={handleUserSignOut}>
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Button
                  as={Link}
                  to="/signin"
                  variant="outline-primary"
                  className="me-2"
                >
                  Sign In
                </Button>
                <Button as={Link} to="/signup" variant="primary">
                  Sign Up
                </Button>
              </>
            )}
          </Nav>
        </BsNav.Collapse>
      </Container>
    </BsNav>
  );
};

export default Navbar;
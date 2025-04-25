// @ts-nocheck
import { useEffect, useState, createContext } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import { ToastContainer } from 'react-toastify';
import { Spinner } from 'react-bootstrap';

import Home from './pages/Home';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Listings from './pages/Listings';
import PetDetail from './pages/PetDetail';
import ApplyForm from './pages/ApplyForm';
import MyApplications from './pages/MyApplications';
import ProtectedRoute from './components/ProtectedRoute';

import AdminSignIn from './admin/AdminSignIn';
import Dashboard from './admin/Dashboard';
import AdminProtectedRoute from './admin/AdminProtectedRoute';

import { getSession } from './api/auth';

export const AuthContext = createContext<{ username: string } | null>(null);
export const AdminContext = createContext<{ admin: string } | null>(null);

function App() {
  const [user, setUser]   = useState<{ username: string } | null>(null);
  const [admin, setAdmin] = useState<{ admin: string }    | null>(null);
  const [loadingSession, setLoadingSession] = useState(true);

  // load user session on mount; clear admin if user is found
  useEffect(() => {
    getSession()
      .then(u => {
        if (u) {
          setUser({ username: u });
          setAdmin(null);
        } else {
          setUser(null);
        }
      })
      .finally(() => setLoadingSession(false));
  }, []);

  if (loadingSession) {
    return <div className="d-flex justify-content-center align-items-center" style={{height: '100vh'}}><Spinner animation="border" /></div>;
  }

  return (
    <AdminContext.Provider value={admin}>
      <AuthContext.Provider value={user}>
        <Navbar />

        <ToastContainer position="top-right" />
        <div className="container mt-4">
          <Routes>
            {/* Public / User routes */}
            <Route path="/" element={<Home />} />
            <Route
              path="/signin"
              element={
                <SignIn
                  onLogin={u => {
                    setUser(u);
                    setAdmin(null);
                  }}
                />
              }
            />
            <Route
              path="/signup"
              element={
                <SignUp
                  onSignup={u => {
                    setUser(u);
                    setAdmin(null);
                  }}
                />
              }
            />
            <Route path="/listings" element={<Listings />} />
            <Route path="/pets/:id" element={<PetDetail />} />
            <Route
              path="/apply/:id"
              element={
                <ProtectedRoute>
                  <ApplyForm />
                </ProtectedRoute>
              }
            />
            <Route
              path="/applications"
              element={
                <ProtectedRoute>
                  <MyApplications />
                </ProtectedRoute>
              }
            />

            {/* Admin routes */}
            <Route
              path="/admin/signin"
              element={
                <AdminSignIn
                  onAdminLogin={(admin: string) => {
                    setAdmin({ admin });
                    setUser(null);
                  }}
                />
              }
            />
            <Route
              path="/admin/dashboard"
              element={
                <AdminProtectedRoute>
                  <Dashboard />
                </AdminProtectedRoute>
              }
            />
          </Routes>
        </div>
      </AuthContext.Provider>
    </AdminContext.Provider>
  );
}

export default App;

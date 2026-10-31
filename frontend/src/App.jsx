
import { Routes, Route, Navigate } from 'react-router-dom';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';

import PatientDashboard from './pages/PatientDashboard';
import CaregiverDashboard from './pages/CaregiverDashboard';

import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/patient"
        element={
          <ProtectedRoute allowedRole="patient">
            <PatientDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/caregiver"
        element={
          <ProtectedRoute allowedRole="caregiver">
            <CaregiverDashboard />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;

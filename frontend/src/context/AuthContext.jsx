
import {
  createContext,
  useContext,
  useEffect,
  useState
} from 'react';

import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('user')) || null;
    } catch {
      return null;
    }
  });

  const [loading, setLoading] = useState(true);

  // Load the caregiver's linked patients and select one.
  const loadLinkedPatient = async () => {
    try {
      const response = await api.get('/linking/patients');
      const patients = response.data.patients || [];

      const currentSelection = localStorage.getItem(
        'selectedPatientId'
      );

      const selectionExists = patients.some(
        (patient) => patient.id === currentSelection
      );

      if (!selectionExists) {
        if (patients.length > 0) {
          localStorage.setItem(
            'selectedPatientId',
            patients[0].id
          );
        } else {
          localStorage.removeItem('selectedPatientId');
        }
      }

      return patients;
    } catch (error) {
      console.error('Unable to load linked patients:', error);
      return [];
    }
  };

  // Verify an existing session when the application loads.
  useEffect(() => {
    const verifySession = async () => {
      const token = localStorage.getItem('access_token');

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get('/auth/me');

        setUser(response.data);
        localStorage.setItem(
          'user',
          JSON.stringify(response.data)
        );

        if (response.data.role === 'caregiver') {
          await loadLinkedPatient();
        }
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('selectedPatientId');

        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    verifySession();
  }, []);

  // Save authentication details after successful login or registration.
  const saveSession = (data) => {
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    setUser(data.user);
  };

  // Login
  const login = async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password
    });

    saveSession(response.data);

    if (response.data.user.role === 'caregiver') {
      await loadLinkedPatient();
    }

    return response.data.user;
  };

  // Registration
  const register = async (name, email, password, role) => {
    const response = await api.post('/auth/register', {
      name,
      email,
      password,
      role
    });

    saveSession(response.data);

    if (response.data.user.role === 'caregiver') {
      await loadLinkedPatient();
    }

    return response.data.user;
  };

  // Logout
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    localStorage.removeItem('selectedPatientId');

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: Boolean(user),
        login,
        register,
        logout,
        loadLinkedPatient
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom authentication hook.
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      'useAuth must be used inside AuthProvider'
    );
  }

  return context;
}

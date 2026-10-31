
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Attach the current JWT to every API request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Caregiver requests must identify the selected linked patient.
const patientParams = () => {
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  if (user?.role === 'caregiver') {
    const patientId = localStorage.getItem('selectedPatientId');

    return patientId
      ? { params: { patient_id: patientId } }
      : { params: {} };
  }

  return {};
};

// Authentication
export const loginUser = async (data) => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const registerUser = async (data) => {
  const response = await api.post('/auth/register', data);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Patient-caregiver linking
export const getLinkedPatients = async () => {
  const response = await api.get('/linking/patients');
  return response.data;
};

export const generateLinkingCode = async () => {
  const response = await api.post('/linking/code');
  return response.data;
};

export const redeemLinkingCode = async (code) => {
  const response = await api.post('/linking/redeem', { code });
  return response.data;
};

export const selectPatient = (patientId) => {
  localStorage.setItem('selectedPatientId', patientId);
};

// Memories
export const getMemories = async () => {
  const response = await api.get('/memories/', patientParams());
  return response.data;
};

export const createMemory = async (data) => {
  const response = await api.post('/memories/', data, patientParams());
  return response.data;
};

export const updateMemory = async (id, data) => {
  const response = await api.put(
    `/memories/${id}`,
    data,
    patientParams()
  );
  return response.data;
};

export const deleteMemory = async (id) => {
  const response = await api.delete(
    `/memories/${id}`,
    patientParams()
  );
  return response.data;
};

// Reminders
export const getReminders = async () => {
  const response = await api.get('/reminders/', patientParams());
  return response.data;
};

export const createReminder = async (data) => {
  const response = await api.post('/reminders/', data, patientParams());
  return response.data;
};

export const updateReminder = async (id, data) => {
  const response = await api.put(
    `/reminders/${id}`,
    data,
    patientParams()
  );
  return response.data;
};

export const deleteReminder = async (id) => {
  const response = await api.delete(
    `/reminders/${id}`,
    patientParams()
  );
  return response.data;
};

// Chat
export const sendChatMessage = async (message) => {
  const response = await api.post('/chat/', { message });
  return response.data;
};

// Conversation history and caregiver summary
export const getConversations = async () => {
  const response = await api.get(
    '/conversations/',
    patientParams()
  );
  return response.data;
};

export const getConversationSummary = async () => {
  const response = await api.get(
    '/conversations/summary',
    patientParams()
  );
  return response.data;
};

export default api;

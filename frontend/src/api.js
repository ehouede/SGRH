import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (username, password) => api.post('/token/', { username, password });
export const getEmployes = () => api.get('/employes/');
export const getContratPdfUrl = (id) => `${API_URL}/employes/${id}/generer_contrat/`;
export const getContrats = () => api.get('/contrats/');

export const getPublicOffres = () => axios.get(`${API_URL}/recrutement/public-offres/`);
export const genererPaie = (employeId, periode) => api.post('/paie/bulletins/generer/', { employe_id: employeId, periode });
export const getBulletins = () => api.get('/paie/bulletins/');
export const getBulletinPdfUrl = (id) => `${API_URL}/paie/bulletins/${id}/telecharger_pdf/`;

export const getTypesConge = () => api.get('/conges/types/');
export const getDemandesConge = () => api.get('/conges/demandes/');
export const creerDemandeConge = (data) => api.post('/conges/demandes/', data);

export const getOffres = () => api.get('/recrutement/offres/');
export const getCandidatures = () => api.get('/recrutement/candidatures/');
export const updateCandidature = (id, data) => api.patch(`/recrutement/candidatures/${id}/`, data);

export const getStats = () => api.get('/employes/stats/');
export const getCurrentUser = () => api.get('/employes/me/');
export const getPointages = () => api.get('/pointages/');
export const getObjectifs = () => api.get('/objectifs/');

export default api;

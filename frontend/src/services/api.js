import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

// ===== Colis =====
export const colisApi = {
  lister: () => api.get('/api/colis').then(r => r.data),
  obtenir: (id) => api.get(`/api/colis/${id}`).then(r => r.data),
  creer: (data) => api.post('/api/colis', data).then(r => r.data),
  supprimer: (id) => api.delete(`/api/colis/${id}`),
  transiter: (id, nouvel_etat, commentaire = '') =>
    api.post(`/api/colis/${id}/transiter`, { nouvel_etat, commentaire }).then(r => r.data),
  historique: (id) => api.get(`/api/colis/${id}/historique`).then(r => r.data),
}

// ===== Livreurs =====
export const livreursApi = {
  lister: () => api.get('/api/livreurs').then(r => r.data),
  creer: (data) => api.post('/api/livreurs', data).then(r => r.data),
}

// ===== Routage =====
export const routageApi = {
  calculer: (data) => api.post('/api/routes/calculer', data).then(r => r.data),
  strategies: () => api.get('/api/strategies').then(r => r.data),
  graphe: () => api.get('/api/graphe').then(r => r.data),
}

export default api

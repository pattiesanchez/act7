const apiBase = (import.meta.env.VITE_API_URL?.trim() || '/api/v1').replace(/\/+$/, '')

export function apiUrl(path) {
  return `${apiBase}/${path}`
}

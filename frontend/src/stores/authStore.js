import { defineStore } from 'pinia'

const storageKeys = {
  id: 'receitas_flaites_id',
  name: 'receitas_flaites_nome',
  token: 'receitas_flaites_token',
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authId: localStorage.getItem(storageKeys.id),
    authNome: localStorage.getItem(storageKeys.name),
    authToken: localStorage.getItem(storageKeys.token),
  }),

  actions: {
    iniciarSecao({ id, nome, token }) {
      localStorage.setItem(storageKeys.id, id)
      localStorage.setItem(storageKeys.name, nome)
      localStorage.setItem(storageKeys.token, token)
      this.authId = String(id)
      this.authNome = nome
      this.authToken = token
    },

    encerrarSecao() {
      if (!window.confirm('Deseja realmente sair?')) return false

      Object.values(storageKeys).forEach((key) => localStorage.removeItem(key))
      this.authId = null
      this.authNome = null
      this.authToken = null
      return true
    },
  },
})

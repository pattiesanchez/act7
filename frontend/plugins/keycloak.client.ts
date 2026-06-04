import Keycloak from 'keycloak-js'

export default defineNuxtPlugin(async () => {
  const keycloak = new Keycloak({
    url: 'http://localhost:8080',
    realm: 'act7',
    clientId: 'act7-frontend',
  })

  try {
    await keycloak.init({
      onLoad: 'check-sso',
      checkLoginIframe: false,
    })

    return {
      provide: {
        keycloak,
      },
    }
  } catch (error) {
    console.error('Erro ao inicializar Keycloak', error)
  }
})
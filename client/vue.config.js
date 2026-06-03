const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/promotionen': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/fnk': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})

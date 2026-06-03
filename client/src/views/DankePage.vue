<template>
  <div class="danke-container">
    <div class="nav-bar">
      <button class="logout-btn" @click="logout">Abmelden</button>
    </div>

    <h2>Vielen Dank!</h2>
    <p>Ihr Antrag wurde erfolgreich übermittelt und wird geprüft.</p>
    <button class="home-btn" @click="goHome">Zur Homepage</button>
  </div>
</template>

<script>
export default {
  name: 'DankePage',
  methods: {
    goHome() {
      this.$router.push('/home');
    },
    logout() {
      localStorage.removeItem('user');
      localStorage.removeItem('userId');
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.danke-container {
  text-align: center;
  margin-top: 100px;
  position: relative;
}
.nav-bar {
  position: absolute;
  top: 20px;
  right: 30px;
}

.logout-btn {
  font-size: 14px;
  background-color: #e53935;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}
.logout-btn:hover {
  background-color: #c62828;
}
.home-btn {
  margin-top: 20px;
  padding: 12px 20px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}
.home-btn:hover {
  background-color: #1565c0;
}
</style>

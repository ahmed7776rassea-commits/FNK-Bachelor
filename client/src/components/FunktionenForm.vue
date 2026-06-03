<template>
  <div class="box">
  
    <div class="nav-bar">
      <button class="home-btn" @click="goToHome">Home</button>
      <button class="logout-btn" @click="logout">Abmelden</button>
    </div>

    <div class="content">
      <h1>Die funktionalen Anforderungen Typen</h1>
      <div class="buttons">
        <button @click="goTo('antrag1')">Antragsart 1:<br />Drittmittelfinanziertes Vorhaben</button>
        <button @click="goTo('antrag2ab')">Antragsart 2:<br />Veröffentlichungen und<br />künstlerische Präsentation/Publikation</button>
        <button @click="goTo('antraga3ab')">Antragsart 3:<br />Beginn Promotionsvorhaben<br />und Abschluss Promotionsvorhaben</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FunktionenForm',
  methods: {
    goTo(route) {
      this.$router.push(`/${route}`);
    },
    goToHome() {
      this.$router.push('/home');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.box {
  background-color: white;
  height: 100vh;
  background-image: url('@/assets/htw2.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  position: relative;
}

.nav-bar {
  position: absolute;
  top: 20px;
  right: 30px; 
  display: flex;
  gap: 10px;
  align-items: center;
}

.home-btn {
  font-size: 14px;
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.home-btn:hover {
  background-color: #1565c0;
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

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

h1 {
  color: black;
  font-size: 28px;
  text-align: center;
}

.buttons {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.buttons button {
  width: 300px;
  height: 200px;
  font-weight: bold;
  transition: transform 0.3s ease, background-color 0.3s ease;
  border: none;
  background-color: #4CAF50;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.buttons button:hover {
  transform: scale(1.05);
  background-color: #45a049;
}

.buttons button:active {
  transform: scale(0.95);
}
</style>

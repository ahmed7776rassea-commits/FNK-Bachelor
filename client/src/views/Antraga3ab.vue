<template>
  <div class="box">


    <div class="content">
      <h1>Beginn Promotionsvorhaben Antragsart und Abschluss Promotionsvorhaben</h1>
      <div class="buttons">
        <button @click="goTo('antrag3a')">Antragsart 3a:Beginn Promotionsvorhaben </button>
        <button @click="goTo('antrag3b')">Antragsart 3b:Abschluss Promotionsvorhaben </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FunktionenZweiab',
  methods: {
    goTo(route) {
      this.$router.push(`/${route}`);
    },
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
}

.home-link {
  font-size: 18px; 
  color: #333;
  text-decoration: underline;
  font-weight: bold;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 5px;
  transition: color 0.3s;
}

.home-link:hover {
  color: #1976d2;
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

button {
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

button:hover {
  transform: scale(1.05);
  background-color: #45a049;
}

button:active {
  transform: scale(0.95);
}
</style>
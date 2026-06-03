<template>
  <div class="container">
    <div class="logo-box">
      <img src="@/assets/htw1.png" alt="HTW Logo" />
    </div>

    <div class="login-box">
      <h1>
        Willkommen bei Kommission <br />
        für Forschung <br />
        und wissenschaftlichen <br />
        Nachwuchs (FNK)
      </h1>
      <h2>Anmeldung</h2>
      <form @submit.prevent="handleLogin">
        <input type="text" v-model="username" placeholder="Benutzername" required />
        <input type="password" v-model="password" placeholder="Passwort" required />
        <button type="submit">Anmelden</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    handleLogin() {
      const formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);

      fetch("http://localhost:8000/auth/login", {
        method: "POST",
        body: formData
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Anmeldung fehlgeschlagen.");
          }
          return response.json();
        })
        .then(data => {
          localStorage.setItem("userId", data.benutzer_id);
          localStorage.setItem("user", JSON.stringify({
            name: data.name,
            nachname: data.nachname,
            email: data.email,
            rolle: data.rolle,
          }));

          if (data.rolle.toLowerCase() === "antragsteller") {
            this.$router.push('/hinweise');
          } else if (data.rolle.toLowerCase() === "fnk") {
            this.$router.push('/fnk');
          } else {
            this.$router.push('/');
          }
        })
        .catch(error => {
          alert("Fehler beim Login: " + error.message);
        });
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/htw2.jpg');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  font-family: 'Arial', sans-serif;
  position: relative;
}

.logo-box {
  position: fixed;
  top: 15px;
  left: 15px;
  z-index: 1000;
}
.logo-box img {
  width: 150px;
  height: 150px;
  object-fit: contain;
  border-radius: 15px;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}


.login-box {
  background-color: white;
  padding: 20px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px; 
  text-align: center;
  direction: ltr;
}

h1 {
  margin-bottom: 10px;
  color: green;
  font-size: 20px; 
  line-height: 1.4;
}

h2 {
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #1565c0;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0d47a1;
}
</style>


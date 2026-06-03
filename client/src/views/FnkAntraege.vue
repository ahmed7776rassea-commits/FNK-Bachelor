<template>
  <div class="fnk-antraege">
    <div class="nav-bar">
      <button class="home-btn" @click="goHome">Home</button>
      <button class="apply-btn" @click="goFunktionen">Antrag stellen</button>
      <button class="logout-btn" @click="logout">Abmelden</button>
    </div>

    <h2>Alle Anträge (FNK Ansicht)</h2>

    <ul v-if="antraege.length > 0">
      <li v-for="antrag in antraege" :key="antrag.antrag_id" @click="openDetail(antrag)">
        <strong class="clickable">
          {{ antrag.benutzer?.name }} {{ antrag.benutzer?.nachname }}
        </strong><br />
        {{ labelForTyp(antrag.antrag_typ) }} |
        {{ displayLine(antrag) }}
      </li>
    </ul>
    <p v-else>Keine Anträge vorhanden.</p>
  </div>
</template>

<script>
export default {
  name: 'FnkAntraege',
  data() {
    return { antraege: [] }
  },
  created() { this.loadAntraege() },
  beforeRouteEnter(to, from, next) { next(vm => vm.loadAntraege()) },
  methods: {
    async loadAntraege() {
      try {
        const res = await fetch("http://localhost:8000/fnk/antraege")
        const data = await res.json()
        this.antraege = Array.isArray(data) ? data : []
      } catch (e) {
        console.error(e)
        this.antraege = []
      }
    },
    
    labelForTyp(t) {
      const n = Number(t)
      const map = {
        1: 'Antrag 1',
        2: 'Antrag 2a',
        3: 'Antrag 2b',
        4: 'Antrag 3a',
        5: 'Antrag 3b'
      }
      return map[n] || `Antrag ${t}`
    },
    
    displayLine(a) {
      const lines = []

      if (a.pruefer_eins)
        lines.push(`Bereits geprüft von ${a.pruefer_eins} — Status: ${a.status_eins || a.status || '—'}`)

      if (a.pruefer_zwei)
        lines.push(`Bereits geprüft von ${a.pruefer_zwei} — Status: ${a.status_zwei || a.status || '—'}`)

      if (!lines.length && Array.isArray(a.pruefer) && a.pruefer.length)
        lines.push(`Bereits geprüft von ${a.pruefer.join(', ')} — Status: ${a.status || '—'}`)

      if (!lines.length)
        lines.push(`Status: ${a.status || a.status_eins || a.status_zwei || 'Offen'}`)

      return lines.join('  •  ')
    },
    openDetail(antrag) { this.$router.push({ name: 'FnkDetail', params: { id: antrag.antrag_id } }) },
    goHome() { this.$router.push('/home') },
    goFunktionen() { this.$router.push('/funktionen') },
    logout() {
      
      localStorage.removeItem('user')
      localStorage.removeItem('userId')
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.fnk-antraege {
  max-width: 800px;
  margin: auto;
  padding: 80px 30px 30px 30px;
  position: relative;
  font-family: Arial, sans-serif;
}


.nav-bar {
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 8px;
}


.home-btn,
.apply-btn,
.logout-btn {
  font-size: 14px;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color .2s ease, opacity .2s ease;
}


.home-btn { background-color: #1976d2; color: #fff; }
.home-btn:hover { background-color: #1565c0; }

.apply-btn { background-color: #16a34a; color: #fff; }
.apply-btn:hover { background-color: #15803d; }

.logout-btn { background-color: #e53935; color: #fff; }
.logout-btn:hover { background-color: #c62828; }

h2 { margin-top: 0; }

ul { padding: 0; list-style: none; }
li {
  background: #f9f9f9;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
li:hover { background: #e6f7ff; }

.clickable { color: #2e7d32; font-size: 18px; }
</style>

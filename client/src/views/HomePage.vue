<template>
  <section class="wrap" v-if="loaded">
    <header class="head">
      <div class="user-box" v-if="user">
        <h2>Willkommen, {{ user.name }} {{ user.nachname }}</h2>
        <p>Name: {{ user.name }}</p>
        <p>Nachname: {{ user.nachname }}</p>
        <p>Email: {{ user.email }}</p>
      </div>

      
      <div class="filters">
        <select v-model="filterTyp">
          <option value="">Alle Typen</option>
          <option v-for="t in [1,2,3,4,5]" :key="t" :value="String(t)">Typ {{ t }}</option>
        </select>
        <select v-model="filterStatus">
          <option value="">Alle Status</option>
          <option>Offen</option>
          <option>In Prüfung</option>
          <option>Akzeptiert</option>
          <option>Abgelehnt</option>
        </select>
        <input v-model="q" placeholder="Suche (ID oder Kommentar)..." />
      </div>

      <!-- زر Abmelden -->
      <button class="logout-btn" @click="logout">Abmelden</button>
    </header>

    <div class="card">
      <h3 class="section-title"> Verlauf  Deine Anträge</h3>
      <table class="tbl" v-if="filtered.length">
        <thead>
          <tr>
            <th>Typ</th>
            <th>Status</th>
            <th>Punkte</th>
            <th>Letzter Kommentar</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filtered" :key="row.Antrag_id">
            <td>{{ labelForTyp(row.Antrag_typ) }}</td>
            <td>
              {{ row.Status_eins }}
              <span v-if="row.Status_zwei">/ {{ row.Status_zwei }}</span>
            </td>
            <td><strong>{{ fmtPts(row.Punkte) }}</strong></td>
            <td class="comment">
              <em v-if="!row.Letzter_Kommentar?.text"></em>
              <span v-else>{{ cut(row.Letzter_Kommentar.text, 80) }}</span>
              <div class="comment-date" v-if="row.Letzter_Kommentar?.zeit">
                {{ fmtDate(row.Letzter_Kommentar.zeit) }}
              </div>
            </td>
            <td class="actions">
              <router-link :to="`/verlauf/${row.Antrag_id}`">Ansehen →</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else><em>Keine Anträge gefunden.</em></p>
    </div>
  </section>

  <section v-else class="wrap">
    <div class="card"><em>Lade…</em></div>
  </section>
</template>

<script>
export default {
  name: "VerlaufPage",
  data() {
    return {
      loaded: false,
      user: null,
      rows: [],
      filterTyp: "",
      filterStatus: "",
      q: ""
    };
  },
  computed: {
    filtered() {
      return this.rows.filter(r => {
        if (this.filterTyp && String(r.Antrag_typ) !== this.filterTyp) return false;
        if (this.filterStatus && r.Status_eins !== this.filterStatus) return false;
        if (this.q) {
          const hay = `${r.Antrag_id} ${r.Letzter_Kommentar?.text || ''}`.toLowerCase();
          if (!hay.includes(this.q.toLowerCase())) return false;
        }
        return true;
      });
    }
  },
  methods: {
    labelForTyp(t) {
      const map = {
        1: "Antrag 1",
        2: "Antrag 2a",
        3: "Antrag 2b",
        4: "Antrag 3a",
        5: "Antrag 3b"
      };
      return map[t] || `Antrag ${t}`;
    },
    fmtDate(d) {
      if (!d) return "";
      try {
        return new Date(d).toLocaleString("de-DE");
      } catch {
        return d;
      }
    },
    fmtPts(n) {
      return (Number(n || 0)).toFixed(1);
    },
    cut(s, n) {
      return s && s.length > n ? s.slice(0, n) + "…" : s;
    },
    loadUser() {
      const u = localStorage.getItem("user");
      if (u) {
        const j = JSON.parse(u);
        this.user = {
          name: j.name || j.Name || "",
          nachname: j.nachname || j.Nachname || "",
          email: j.email || j.Email || ""
        };
      }
    },
    async loadRows() {
      const userId = localStorage.getItem("userId");
      if (!userId) {
        this.loaded = true;
        return;
      }
      const res = await fetch(`http://localhost:8000/verlauf/me/${userId}`);
      this.rows = await res.json();
      this.loaded = true;
    },
    logout() {
      localStorage.removeItem("user");
      localStorage.removeItem("userId");
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },
  mounted() {
    this.loadUser();
    this.loadRows();
  }
};
</script>

<style scoped>
.wrap{ max-width:1000px; margin:22px auto; padding:0 12px; font-family:Arial, sans-serif; }
.head{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px; gap:12px; flex-wrap:wrap; }
.user-box{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:12px 14px; min-width:280px; }
.user-box h2{ margin:0 0 6px; }
.filters{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.filters select, .filters input{ padding:8px; border:1px solid #cbd5e1; border-radius:8px; }
.card{ background:#fff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,.08); padding:16px; }
.section-title{ margin-top:0; }
.tbl{ width:100%; border-collapse:collapse; }
.tbl th, .tbl td{ padding:10px; border-bottom:1px solid #eef2f7; text-align:left; }
.tbl tbody tr:hover{ background:#fafafa; }
.actions a{ text-decoration:none; font-weight:700; }
.comment{ max-width:380px; }
.comment-date{ font-size:12px; opacity:.7; margin-top:2px; }

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
</style>

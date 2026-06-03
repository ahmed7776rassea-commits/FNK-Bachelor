<template>
  <section class="wrap" v-if="loaded">
    <button class="back" @click="$router.back()">← Zurück</button>

    <header class="card">
      <h2>{{ labelForTyp(meta.typ) }}</h2>
      <div class="meta">
        <div>
          <strong>Status:</strong>
          {{ meta.status_eins }}<span v-if="meta.status_zwei"> / {{ meta.status_zwei }}</span>
        </div>
        
        <div class="score">
          <div class="score-value">{{ totalPoints }}</div>
          <div class="score-label">Punkte gesamt</div>
        </div>
      </div>
    </header>

    <article class="card">
      <h3>Angaben</h3>
      <div v-if="fieldList.length">
        <div v-for="f in fieldList" :key="f.key" class="field">
          <div class="label">
            {{ f.label }}
            <span v-if="pointsFor(f.key) !== null" class="badge">+{{ pointsFor(f.key) }}</span>
          </div>

          <div class="value">
            <template v-if="f.type === 'money'">
              {{ fmtMoney(data[f.key]) }}
            </template>

            <template v-else-if="f.type === 'bool'">
              {{ yesno(data[f.key]) }}
            </template>

            <template v-else-if="f.type === 'zusatz'">
              <template v-if="prettyZusatz(data[f.key]).length">
                <ul class="zusatz-list">
                  <li v-for="([k, v], i) in prettyZusatz(data[f.key])" :key="i">
                    <strong>{{ k }}:</strong> <span>{{ v }}</span>
                  </li>
                </ul>
              </template>
              <em v-else>–</em>
            </template>

            <template v-else>
              {{ data[f.key] }}
            </template>
          </div>
        </div>
      </div>
      <div v-else><em>Für diesen Typ sind noch keine Felder konfiguriert.</em></div>
    </article>

    <article class="card">
      <h3>Dateien</h3>
      <ul class="files" v-if="files.length">
        <li v-for="f in files" :key="f.id">
          <a :href="f.pfad" target="_blank" rel="noopener"> {{ f.name || ('Datei #' + f.id) }}</a>
        </li>
      </ul>
      <p v-else><em>Keine Dateien vorhanden.</em></p>
    </article>

    <article class="card">
      <h3>Kommentare (FnK)</h3>
      <ul class="comments" v-if="kommentare.length">
        <li v-for="k in kommentare" :key="k.id">
          <div class="k-text">{{ k.text }}</div>
          <div class="k-meta">{{ fmtDate(k.zeit) }}</div>
        </li>
      </ul>
      <p v-else><em>Noch keine Kommentare.</em></p>
    </article>
  </section>

  <section v-else class="wrap">
    <div class="card"><em>Lade Daten…</em></div>
  </section>
</template>

<script>
const FIELDS = {
  '1': [
    { key: 'titel', label: 'Titel des Vorhabens' },
    { key: 'fachbereich', label: 'Fachbereich' },
    { key: 'beginn', label: 'Beginn' },
    { key: 'ende', label: 'Ende' },
    { key: 'drittmittelgeber', label: 'Drittmittelgeber' },
    { key: 'gesamtmittel', label: 'HTW-Anteil Gesamt (€)', type: 'money' },
    { key: 'zugeordnet', label: 'Zugeordnete Drittmittel (€)', type: 'money' },
    { key: 'verfuegbar', label: 'Verfügbare Mittel (€)', type: 'money' },
    { key: 'eingesetzt', label: 'Eingesetzt im Semester (€)', type: 'money' },
    { key: 'nebentaetigkeit', label: 'Keine Nebentätigkeit', type: 'bool' }
  ],
  '2': [
    { key: 'titel_veroeffentlichung', label: 'Titel der Veröffentlichung' },
    { key: 'fachbereich', label: 'Fachbereich' },
    { key: 'bibliographische_angaben', label: 'Bibliographische Angaben' },
    { key: 'erscheinungsdatum', label: 'Erscheinungsdatum' },
    { key: 'alleinautor', label: 'Alleinautorenschaft', type: 'bool' },
    { key: 'koautor', label: 'Koautorschaft', type: 'bool' },
    { key: 'peer_review', label: 'Peer Review', type: 'bool' },
    { key: 'drittbegutachtung', label: 'Inhaltliche Begutachtung', type: 'bool' },
    { key: 'einnahmen_nebentaetigkeit', label: 'Keine Einnahmen aus Nebentätigkeit', type: 'bool' }
  ],
  '3': [
    { key: 'titel_praesentation', label: 'Titel/Präsentation' },
    { key: 'fachbereich', label: 'Fachbereich' },
    { key: 'erscheinungsdatum', label: 'Datum der Veranstaltung/Erscheinung' },
    { key: 'beteiligung', label: 'Beteiligung' },
    { key: 'format_a', label: 'Format A', type: 'bool' },
    { key: 'format_b', label: 'Format B', type: 'bool' },
    { key: 'format_c', label: 'Format C', type: 'bool' },
    { key: 'zusatz_optionen', label: 'Zusatzoptionen', type: 'zusatz' },
    { key: 'einnahmen_nebentaetigkeit', label: 'Keine Einnahmen aus Nebentätigkeit', type: 'bool' }
  ],
  '4': [
    { key: 'antragsteller_name',      label: 'Antragsteller/in' },
    { key: 'beteiligte_universitaet', label: 'Beteiligte Universität' },
    { key: 'promovend_name',          label: 'Name des/der Promovenden' },
    { key: 'arbeitstitel',            label: 'Arbeitstitel der Dissertation' },
    { key: 'beginn_betreuung',        label: 'Beginn lt. Betreuungsvereinbarung' },
    { key: 'zeitraum_von',            label: 'Zeitraum von' },
    { key: 'zeitraum_bis',            label: 'Zeitraum bis' }
  ],
  '5': [
    { key: 'antragsteller_name',      label: 'Antragsteller/in' },
    { key: 'beteiligte_universitaet', label: 'Beteiligte Universität' },
    { key: 'promovend_name',          label: 'Name des/der Promovenden' },
    { key: 'titel_dissertation',      label: 'Titel der Dissertation' },
    { key: 'datum_disp',              label: 'Datum Disputation/Verteidigung' },
    { key: 'zeitraum_von',            label: 'Zeitraum von' },
    { key: 'zeitraum_bis',            label: 'Zeitraum bis' },
    { key: 'einnahmen_nebentaetigkeit', label: 'Keine Einnahmen aus Nebentätigkeit', type: 'bool' }
  ]
}

export default {
  name: 'VerlaufDetail',
  data() {
    return {
      loaded: false,
      meta: {},
      data: {},
      files: [],
      kommentare: [],
      breakdown: {},

      
      optionLabels: {
        FormatTitle: {
          A: 'A. Kuratieren einer Ausstellung',
          B: 'B. Teilnahme an einer Ausstellung / Festival / Modenschau / Performativem Format',
          C: 'C. Künstlerische Publikation (auch online) in Abgrenzung zu den normalen peer-reviewed Papern'
        },
        A_Option: {
          htw_le3:         'an der HTW (öffentlich zugänglich), Dauer ≤ 3 Tage',
          htw_gt3:         'an der HTW (öffentlich zugänglich), Dauer > 3 Tage',
          ausserhalb_leq3: 'außerhalb, Dauer ≤ 3 Tage',
          ausserhalb_gt3:  'außerhalb, Dauer > 3 Tage'
        },
        B_Option: {
          wettbewerb: 'im Wettbewerb',
          einladung:  'auf Einladung'
        },
        katalogText: 'inkl. Herausgabe eines / Publikation im Ausstellungskatalogs'
      }
    }
  },
  computed: {
    fieldList() { return FIELDS[String(this.meta.typ)] || [] },
    totalPoints() { return this.meta.punkte ?? 0 }
  },
  mounted() { this.load() },
  methods: {
    labelForTyp(t) {
      const map = { 1: 'Antrag 1', 2: 'Antrag 2a', 3: 'Antrag 2b', 4: 'Antrag 3a', 5: 'Antrag 3b' }
      return map[t] || `Antrag ${t}`
    },
    fmtMoney(n) {
      if (n == null || n === '') return ''
      const num = Number(n)
      return isFinite(num)
        ? new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(num)
        : n
    },
    yesno(v) { return v ? 'Ja' : 'Nein' },
    fmtDate(d) {
      if (!d) return ''
      try { return new Date(d).toLocaleString('de-DE') } catch { return d }
    },
    computeBreakdown(typ, d) {
      const out = {}
      if (String(typ) === '1') {
        const v = Number(d.eingesetzt || 0)
        let p = 0
        if (v >= 50000) p = 5
        else if (v >= 40000) p = 4
        else if (v >= 30000) p = 3
        else if (v >= 20000) p = 2
        else if (v >= 10000) p = 1
        out.eingesetzt = p
      }
      if (String(typ) === '2') {
        out.alleinautor = d.alleinautor ? 2 : 0
        out.koautor = d.koautor ? 1 : 0
        const gut = d.peer_review ? 2 : (d.drittbegutachtung ? 0.5 : 0)
        const before = out.alleinautor + out.koautor
        const rest = Math.min(4, before + gut) - before
        out.peer_review = d.peer_review ? Math.min(2, rest) : 0
        out.drittbegutachtung = (!d.peer_review && d.drittbegutachtung) ? Math.min(0.5, rest) : 0
      }
      this.breakdown = out
    },
    pointsFor(key) {
      return (key in this.breakdown) ? this.breakdown[key] : null
    },

    
    ensureObject(val) {
      if (!val) return null
      if (typeof val === 'object') return val
      try { return JSON.parse(val) } catch { return null }
    },

    
    prettyZusatz(z) {
      const obj = this.ensureObject(z)
      if (!obj) return []

      const out = []
      const fmt = obj.Format  

      if (fmt === 'A') {
        out.push(['Format', this.optionLabels.FormatTitle.A])

        if (obj.A_Option) {
          const label = this.optionLabels.A_Option[obj.A_Option] || obj.A_Option
          out.push(['Ort/Dauer', label])
        }
        
        if (obj.A_Katalog === true) {
          out.push(['Zusatz', this.optionLabels.katalogText])
        }

      } else if (fmt === 'B') {
        out.push(['Format', this.optionLabels.FormatTitle.B])

        if (obj.B_Option) {
          const label = this.optionLabels.B_Option[obj.B_Option] || obj.B_Option
          out.push(['Modus', label])
        }
        if (obj.B_Katalog === true) {
          out.push(['Zusatz', this.optionLabels.katalogText])
        }

      } else if (fmt === 'C') {
        
        out.push(['Format', this.optionLabels.FormatTitle.C])
        
      }

      return out
    },

    normalize(json) {
      return {
        meta: json.meta,
        data: json.data || {},
        files: json.files || [],
        kommentare: json.kommentare || []
      }
    },
    async load() {
      try {
        const userId = localStorage.getItem('userId')
        const id = this.$route.params.id
        const res = await fetch(`http://localhost:8000/verlauf/me/${userId}/antrag/${id}`)
        if (!res.ok) {
          const txt = await res.text().catch(()=> '')
          throw new Error(`HTTP ${res.status}: ${txt || res.statusText}`)
        }
        const json = await res.json()
        const norm = this.normalize(json)
        this.meta = norm.meta
        this.data = norm.data
        this.files = norm.files
        this.kommentare = norm.kommentare
        this.computeBreakdown(this.meta.typ, this.data)
      } catch (e) {
        console.error(e)
      } finally {
        this.loaded = true
      }
    }
  }
}
</script>

<style scoped>
.wrap { max-width: 1000px; margin: 24px auto; padding: 0 12px; font-family: Arial, sans-serif; }
.back { margin-bottom: 10px; border: none; background: #e5e7eb; border-radius: 8px; padding: 6px 10px; cursor: pointer; }
.card { background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.08); padding: 18px; margin-bottom: 14px; }
.meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; }
.score { display:inline-flex; align-items:center; gap:10px; padding:8px 12px; border:1px solid #d1fae5; background:#ecfdf5; border-radius:10px; }
.score-value { font-size:22px; font-weight:800; color:#065f46; }
.score-label { font-size:12px; color:#065f46; }

.field { display:grid; grid-template-columns:260px 1fr; gap:12px; padding:8px 0; border-bottom:1px solid #f1f5f9; }
.field:last-child { border-bottom:none; }
.field .label { color:#475569; font-weight:700; display:flex; gap:8px; align-items:center; }
.field .value { color:#0f172a; }
.badge { display:inline-block; font-size:12px; padding:2px 8px; border-radius:999px; background:#eef2ff; color:#3730a3; border:1px solid #c7d2fe; }

.files { list-style:none; padding:0; margin:0; }
.files li { margin:6px 0; }

.comments { list-style:none; padding:0; margin:0; }
.comments li { border-bottom:1px solid #f1f5f9; padding:8px 0; }
.k-text { white-space:pre-wrap; }
.k-meta { font-size:12px; opacity:.7; margin-top:4px; }


.zusatz-list { list-style:none; padding:0; margin:0; }
.zusatz-list li { display:flex; gap:.5rem; padding:4px 0; border-bottom:1px solid #f1f5f9; }
.zusatz-list li:last-child { border-bottom:0; }
</style>

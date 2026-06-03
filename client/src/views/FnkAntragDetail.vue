<template>
  <section class="wrap" v-if="loaded">
    <button class="back" @click="$router.back()">← Zurück</button>

    <header class="card">
      <h2>{{ labelForTyp(meta.typ) }}</h2>
      <div class="meta">
        <div><strong>Antragsteller:</strong> {{ meta.benutzer?.name }} {{ meta.benutzer?.nachname }}</div>
        <div><strong>Email:</strong> {{ meta.benutzer?.email }}</div>
        <div>
          <strong>Status:</strong>
          <span v-if="meta.status_eins">{{ meta.status_eins }}</span>
          <span v-if="meta.status_zwei"> / {{ meta.status_zwei }}</span>
        </div>
        <div v-if="isFinal" class="final-badge">Finalisiert</div>
      </div>

      <div class="score">
        <div class="score-value">{{ totalPoints }}</div>
        <div class="score-label">Punkte gesamt</div>
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
            <template v-if="f.type === 'money'">{{ fmtMoney(data[f.key]) }}</template>
            <template v-else-if="f.type === 'bool'">{{ yesno(data[f.key]) }}</template>
            <template v-else-if="f.type === 'zusatz'">
              <template v-if="prettyZusatz(data[f.key]).length">
                <ul class="zusatz-list">
                  <li v-for="([k, v], i) in prettyZusatz(data[f.key])" :key="i">
                    <strong>{{ k }}:</strong> <span>{{ v }}</span>
                  </li>
                </ul>
              </template>
              <em v-else></em>
            </template>
            <template v-else>{{ data[f.key] }}</template>
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
      <h3>Kommentar & Status</h3>
      <p v-if="meta.pruefer_eins" class="hint">
        Bereits geprüft von: <strong>{{ meta.pruefer_eins }}</strong>
        — Status: <strong>{{ meta.status_eins || '—' }}</strong>
      </p>    
      <p v-if="meta.pruefer_zwei" class="hint">
        Bereits geprüft von: <strong>{{ meta.pruefer_zwei }}</strong>
        — Status: <strong>{{ meta.status_zwei || '—' }}</strong>
      </p>

      <div class="field" v-if="!meta.pruefer_eins">
        <div class="label">Status</div>
        <div class="value">
          <select v-model="status_eins">
            <option>Offen</option>
            <option>In Prüfung</option>
            <option>Akzeptiert</option>
            <option>Abgelehnt</option>
          </select>
        </div>
      </div>

      <div class="field" v-else-if="meta.pruefer_eins && !meta.pruefer_zwei">
        <div class="label">Status (2. Prüfer)</div>
        <div class="value">
          <select v-model="status_zwei">
            <option value=""></option>
            <option>Formell OK</option>
            <option>Nachweise fehlen</option>
            <option>Zurückgestellt</option>
          </select>
        </div>
      </div>

      
      <div v-else class="locked-note">
        Dieser Antrag ist final geprüft und gesperrt.
      </div>

      <div class="comment-form" v-if="!isFinal">
        <input v-model="kommentar" placeholder="Kommentar hinzufügen..." />
        <button @click="saveComment"> Speichern</button>
      </div>
      <div class="comment-form" v-else>
        <input v-model="kommentar" placeholder="Kommentar hinzufügen..." disabled />
        <button disabled>Speichern</button>
      </div>
    </article>
  </section>

  <section v-else class="wrap">
    <div class="card"><em>Lade Daten…</em></div>
  </section>
</template>

<script>
export default {
  name: 'FnkDetail',
  data() {
    return {
      loaded: false,
      meta: {},
      data: {},
      files: [],
      kommentare: [],
      kommentar: '',
      status_eins: 'Offen',
      status_zwei: '',
      breakdown: {},

      FIELDS: {
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
          { key: 'beteiligte_universitaet', label: 'Beteiligte Universität' },
          { key: 'promovend_name', label: 'Name des Promovenden/der Promovendin' },
          { key: 'arbeitstitel', label: 'Arbeitstitel der Dissertation' },
          { key: 'beginn_betreuung', label: 'Beginn lt. Betreuungsvereinbarung' },
          { key: 'zeitraum_von', label: 'Zeitraum von' },
          { key: 'zeitraum_bis', label: 'Zeitraum bis' }
        ],
        '5': [
          { key: 'antragsteller_name', label: 'Antragsteller' },
          { key: 'beteiligte_universitaet', label: 'Beteiligte Universität' },
          { key: 'promovend_name', label: 'Name des Promovenden/der Promovendin' },
          { key: 'titel_dissertation', label: 'Titel der Dissertation' },
          { key: 'datum_disp', label: 'Datum der Disputation' },
          { key: 'zeitraum_von', label: 'Zeitraum von' },
          { key: 'zeitraum_bis', label: 'Zeitraum bis' },
          { key: 'einnahmen_nebentaetigkeit', label: 'Keine Einnahmen aus Nebentätigkeit', type: 'bool' }
        ],
      },

      optionLabels: {
        FormatTitle: {
          A: 'A. Kuratieren einer Ausstellung',
          B: 'B. Teilnahme an Ausstellung/Festival/Modenschau/Performativem Format',
          C: 'C. Künstlerische Publikation (auch online)'
        },
        A_Option: {
          htw_le3: 'an der HTW (öffentlich zugänglich), Dauer ≤ 3 Tage',
          htw_gt3: 'an der HTW (öffentlich zugänglich), Dauer > 3 Tage',
          ausserhalb_leq3: 'außerhalb, Dauer ≤ 3 Tage',
          ausserhalb_gt3: 'außerhalb, Dauer > 3 Tage'
        },
        B_Option: {
          wettbewerb: 'im Wettbewerb',
          einladung: 'auf Einladung'
        },
        katalogText: 'inkl. Herausgabe eines / Publikation im Ausstellungskatalogs'
      }
    }
  },
  computed: {
    fieldList() { return this.FIELDS[String(this.meta.typ)] || [] },
    totalPoints() {
      if (this.meta.punkte != null) return this.meta.punkte
      return Object.values(this.breakdown).reduce((a, b) => a + Number(b || 0), 0)
    },
    isFinal() {
      return !!(this.meta.pruefer_eins && this.meta.pruefer_zwei)
    }
  },
  methods: {
    labelForTyp(t) {
      const n = Number(t)
      const map = { 1: 'Antrag 1', 2: 'Antrag 2a', 3: 'Antrag 2b', 4: 'Antrag 3a', 5: 'Antrag 3b' }
      return map[n] || `Antrag ${t ?? ''}`
    },
    fmtMoney(n) {
      if (n == null || n === '') return ''
      const num = Number(n)
      return isFinite(num) ? new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(num) : n
    },
    yesno(v) { return v ? 'Ja' : 'Nein' },
    pointsFor(key) { return (key in this.breakdown) ? this.breakdown[key] : null },
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
      this.breakdown = out
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
        if (obj.A_Option) out.push(['Ort/Dauer', this.optionLabels.A_Option[obj.A_Option] || obj.A_Option])
        if (obj.A_Katalog === true) out.push(['Zusatz', this.optionLabels.katalogText])
      } else if (fmt === 'B') {
        out.push(['Format', this.optionLabels.FormatTitle.B])
        if (obj.B_Option) out.push(['Modus', this.optionLabels.B_Option[obj.B_Option] || obj.B_Option])
        if (obj.B_Katalog === true) out.push(['Zusatz', this.optionLabels.katalogText])
      } else if (fmt === 'C') {
        out.push(['Format', this.optionLabels.FormatTitle.C])
      }
      return out
    },
    normalize(json) {
      if (json && json.meta) {
        return { meta: json.meta, data: json.data || {}, files: json.files || [], kommentare: json.kommentare || [] }
      }
      return { meta: {}, data: json || {}, files: [], kommentare: [] }
    },
    async load() {
      try {
        const id = this.$route.params.id
        const res = await fetch(`http://localhost:8000/fnk/antrag/${id}`)
        const json = await res.json()
        const norm = this.normalize(json)
        this.meta = norm.meta
        this.data = norm.data
        this.files = norm.files
        this.kommentare = norm.kommentare
        this.status_eins = this.meta.status_eins || 'Offen'
        this.status_zwei = this.meta.status_zwei || ''
        this.computeBreakdown(this.meta.typ, this.data)
      } catch (e) {
        console.error(e)
      } finally {
        this.loaded = true
      }
    },
    async saveComment() {
      try {
        
        if (this.isFinal) {
          alert('Dieser Antrag ist final geprüft.')
          return
        }

        const user = JSON.parse(localStorage.getItem('user') || '{}')
        const full = `${user?.name || ''} ${user?.nachname || ''}`.trim()

        const form = new FormData()
        form.append('kommentar', this.kommentar || '')
        if (!this.meta.pruefer_eins) {
          form.append('status_eins', this.status_eins || '')
        } else {
          form.append('status_zwei', this.status_zwei || '')
        }
        form.append('pruefer_name', full)

        const res = await fetch(`http://localhost:8000/fnk/antrag/${this.meta.antrag_id}/kommentar`, {
          method: 'POST',
          body: form
        })
        if (!res.ok) {
          const msg = await res.text().catch(() => '')
          alert(`Fehler beim Speichern: ${msg || res.status}`)
          return
        }
        this.kommentar = ''
        await this.load()
      } catch (e) {
        console.error(e)
        alert('Netzwerkfehler beim Speichern')
      }
    }
  },
  mounted() { this.load() }
}
</script>

<style scoped>
.wrap{ max-width:1000px; margin:24px auto; padding:0 12px; font-family:Arial, sans-serif; }
.back{ margin-bottom:10px; border:none; background:#e5e7eb; border-radius:8px; padding:6px 10px; cursor:pointer; }
.card{ background:#fff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,.08); padding:18px; margin-bottom:14px; }
.meta{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:8px; align-items:center; }
.final-badge{ justify-self:start; background:#e7f5ff; color:#1c7ed6; border:1px solid #a5d8ff; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:700; }

.score{ margin-top:12px; display:inline-flex; align-items:center; gap:10px; padding:8px 12px; border:1px solid #d1fae5; background:#ecfdf5; border-radius:10px; }
.score-value{ font-size:22px; font-weight:800; color:#065f46; }
.score-label{ font-size:12px; color:#065f46; }

.field{ display:grid; grid-template-columns:260px 1fr; gap:12px; padding:8px 0; border-bottom:1px solid #f1f5f9; }
.field:last-child{ border-bottom:none; }
.field .label{ color:#475569; font-weight:700; display:flex; gap:8px; align-items:center; }
.field .value{ color:#0f172a; }

.badge{ display:inline-block; font-size:12px; padding:2px 8px; border-radius:999px; background:#eef2ff; color:#3730a3; border:1px solid #c7d2fe; }

.files{ list-style:none; padding:0; margin:0; }
.files li{ margin:6px 0; }
.comment-form{ display:flex; gap:8px; margin-top:12px; }
.comment-form input{ flex:1; padding:8px; border:1px solid #cbd5e1; border-radius:8px; }
.comment-form button{ padding:8px 12px; background:#16a34a; color:#fff; border:none; border-radius:8px; cursor:pointer; }
.comment-form button[disabled]{ opacity:.6; cursor:not-allowed; }

.zusatz-list{ list-style:none; padding:0; margin:0; }
.zusatz-list li{ display:flex; gap:.5rem; padding:4px 0; border-bottom:1px solid #f1f5f9; }
.zusatz-list li:last-child{ border-bottom:0; }

.locked-note{ padding:8px 12px; background:#fff7ed; border:1px solid #fed7aa; color:#9a3412; border-radius:8px; margin-bottom:10px; }
</style>

<template>
  <div class="form-container">
    <h2>Antragsart 2b: Künstlerische Präsentationen und Publikationen (max. 4,5 Punkte)</h2>
    <div class="info-box">
      <p>
        <strong>Antragsart 2b:</strong> Ermäßigung von Lehrdeputaten für künstlerische Präsentationen
        und Publikationen, die an der HTW Berlin angefertigt wurden (Affiliation erkennbar), deren
        Erscheinen bis zum Stichtag <b>15.03.</b> bzw. <b>15.09.</b> nicht länger als <b>12 Monate</b>
        zurückliegt und die inhaltlich begutachtet wurden bzw. im Wettbewerb oder auf Einladung
        umgesetzt wurden.
      </p>
      <p>
        Bitte erstellen Sie je Veröffentlichung ein PDF und binden die erforderlichen Nachweise darin ein.
        Bitte beachten Sie die Bearbeitungshinweise.
      </p>
    </div>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Name des/der Antragstellers/in:</label>
        <input v-model="antragsteller_name" required readonly />
      </div>

      <div class="form-group">
        <label>Fachbereich:</label>
        <input v-model="fachbereich" required />
      </div>

      <div class="form-group">
        <label>Titel der Präsentation / Titel und bibliographische Angaben zur Publikation:</label>
        <textarea v-model="titel_praesentation" required></textarea>
      </div>

      <div class="form-group">
        <label>Datum der Veranstaltung / des Erscheinens:</label>
        <input type="date" v-model="erscheinungsdatum" required />
      </div>

      <div class="form-group">
        <label>Beteiligung:</label>
        <div class="inline-options">
          <label class="chip">
            <input type="radio" value="allein" v-model="beteiligung" required />
            allein <span class="chip-pts">2</span>
          </label>
          <span class="oder">oder</span>
          <label class="chip">
            <input type="radio" value="zusammen" v-model="beteiligung" required />
            in Zusammenarbeit <span class="chip-pts">1</span>
          </label>
          <span class="oder">oder</span>
          <label class="chip">
            <input type="radio" value="direction" v-model="beteiligung" required />
            in Zusammenarbeit als Art Direction <span class="chip-pts">2</span>
          </label>
        </div>
      </div>

      <div class="form-group">
        <label>Kreuzen Sie nur eins der 3 Formate (A, B oder C) an*:</label>

        <div class="format-card">
          <div class="format-header">
            <label>
              <input type="radio" value="A" v-model="format" required />
              A. Kuratieren einer Ausstellung
            </label>
            <span class="pts"></span>
          </div>
          <div class="format-table">
            <label class="row">
              <span>
                <input type="radio" value="htw_gt3" v-model="a_option" :disabled="format!=='A'"/>
                an der HTW (öffentlich zugänglich), Dauer &gt; 3 Tage
              </span>
              <span class="pts">1</span>
            </label>
            <label class="row">
              <span>
                <input type="radio" value="ausserhalb_leq3" v-model="a_option" :disabled="format!=='A'"/>
                außerhalb, Dauer ≤ 3 Tage
              </span>
              <span class="pts">1</span>
            </label>
            <label class="row">
              <span>
                <input type="radio" value="ausserhalb_gt3" v-model="a_option" :disabled="format!=='A'"/>
                außerhalb, Dauer &gt; 3 Tage
              </span>
              <span class="pts">2</span>
            </label>
            <label class="row">
              <span>
                <input type="checkbox" v-model="a_katalog" :disabled="format!=='A'"/>
                inkl. Herausgabe eines / Publikation im Ausstellungskatalogs
              </span>
              <span class="pts">0,5</span>
            </label>
          </div>
        </div>

        <div class="format-card">
          <div class="format-header">
            <label>
              <input type="radio" value="B" v-model="format" required />
              B. Teilnahme an einem/r Ausstellung / Festival / Modenschau / Performativem Format
            </label>
            <span class="pts"></span>
          </div>
          <div class="format-table">
            <label class="row">
              <span>
                <input type="radio" value="wettbewerb" v-model="b_option" :disabled="format!=='B'"/>
                im Wettbewerb
              </span>
              <span class="pts">2</span>
            </label>
            <label class="row">
              <span>
                <input type="radio" value="einladung" v-model="b_option" :disabled="format!=='B'"/>
                auf Einladung
              </span>
              <span class="pts">1</span>
            </label>
            <label class="row">
              <span>
                <input type="checkbox" v-model="b_katalog" :disabled="format!=='B'"/>
                inkl. Herausgabe eines / Publikation im Ausstellungskatalogs
              </span>
              <span class="pts">0,5</span>
            </label>
          </div>
        </div>

        <div class="format-card">
          <div class="format-header">
            <label>
              <input type="radio" value="C" v-model="format" required />
              C. Künstlerische Publikation (auch online) in Abgrenzung zu den normalen peer-reviewed Papern
            </label>
            <span class="pts">0,5</span>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>Punkte (automatisch):</label>
        <input :value="punkte" readonly />
      </div>

      <div class="form-group">
        <label>
          <input type="checkbox" v-model="einnahmen_nebentaetigkeit" required />
          Hiermit bestätige ich, dass mit dieser Publikation keine Einnahmen aus Nebentätigkeiten verbunden sind.
        </label>
      </div>

      <div class="form-group">
        <label>Nachweise (PDFs einbinden):</label>
        <input type="file" multiple accept="application/pdf" @change="handleFiles" required />
      </div>

      <div class="hint-box">
        <p>
          Die Durchführung/Teilnahme mit den angegebenen Merkmalen ist im Rahmen des Antrags durch
          die Juryentscheidung/Einladung und einen aussagekräftigen Auszug aus der medialen Berichterstattung
          über die Veranstaltung nachzuweisen.
        </p>
        <p>
          Die Nachweise bzgl. Stattfinden der Veranstaltung mit Ihrem Beitrag sowie Erscheinen des Katalogs
          bzw. der Publikation sind <b>in dieses PDF einzubinden</b> (keine zusätzliche Datei schicken).
        </p>
      </div>

      <div v-if="fehler" class="error">{{ fehler }}</div>
      <button type="submit">Absenden</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Antrag2bForm',
  data() {
    return {
      benutzer_id: '',
      antragsteller_name: '',
      fachbereich: '',
      titel_praesentation: '',
      erscheinungsdatum: '',
      beteiligung: '',
      format: '',
      a_option: '',
      a_katalog: false,
      b_option: '',
      b_katalog: false,
      einnahmen_nebentaetigkeit: false,
      nachweise: [],       
      fehler: ''
    };
  },
  computed: {
    punkte() {
      const beteiligungPts = this.beteiligung === 'allein' ? 2 :
                             this.beteiligung === 'zusammen' ? 1 :
                             this.beteiligung === 'direction' ? 2 : 0;

      let formatPts = 0;
      if (this.format === 'A') {
        if (this.a_option === 'ausserhalb_gt3') formatPts = 2;
        else if (this.a_option === 'htw_gt3' || this.a_option === 'ausserhalb_leq3') formatPts = 1;
        if (this.a_katalog) formatPts += 0.5;
      } else if (this.format === 'B') {
        if (this.b_option === 'wettbewerb') formatPts = 2;
        else if (this.b_option === 'einladung') formatPts = 1;
        if (this.b_katalog) formatPts += 0.5;
      } else if (this.format === 'C') {
        formatPts = 0.5;
      }
      const total = beteiligungPts + formatPts;
      return total > 4.5 ? 4.5 : total;
    }
  },
  watch: {
    format(newVal) {
      if (newVal !== 'A') { this.a_option = ''; this.a_katalog = false; }
      if (newVal !== 'B') { this.b_option = ''; this.b_katalog = false; }
    }
  },
  mounted() {
    const userData = localStorage.getItem("user");
    const userId   = localStorage.getItem("userId");
    if (userData && userId) {
      const parsed = JSON.parse(userData);
      this.benutzer_id = userId;
      this.antragsteller_name = `${parsed.name || ''} ${parsed.nachname || ''}`.trim();
      this.fachbereich = parsed.fachbereich || parsed.studiengang || '';
    }
  },
  methods: {
    handleFiles(e) {
      const files = Array.from(e.target.files || []);
      if (!files.length) { this.nachweise = []; return; }
      const allPdf = files.every(f => f.type === 'application/pdf');
      if (!allPdf) {
        this.fehler = 'Bitte nur PDF-Dateien hochladen.';
        e.target.value = '';
        this.nachweise = [];
        return;
      }
      this.fehler = '';
      this.nachweise = files;
    },
    async submitForm() {
      this.fehler = '';
      if (!this.nachweise.length) {
        this.fehler = 'Bitte laden Sie mindestens ein PDF hoch.';
        return;
      }
      if (this.format === 'A' && !this.a_option) {
        this.fehler = 'Bitte wählen Sie eine Option in A.';
        return;
      }
      if (this.format === 'B' && !this.b_option) {
        this.fehler = 'Bitte wählen Sie eine Option in B.';
        return;
      }

      const fd = new FormData();
      fd.append('Benutzer_id', this.benutzer_id);
      fd.append('Antragsteller_name', this.antragsteller_name);
      fd.append('Fachbereich', this.fachbereich);
      fd.append('Titel_praesentation', this.titel_praesentation);
      fd.append('Erscheinungsdatum', this.erscheinungsdatum);
      fd.append('Beteiligung', this.beteiligung);

      fd.append('Format', this.format);
      fd.append('A_Option', this.a_option);
      fd.append('A_Katalog', String(this.a_katalog));
      fd.append('B_Option', this.b_option);
      fd.append('B_Katalog', String(this.b_katalog));

      fd.append('Einnahmen_nebentaetigkeit', String(this.einnahmen_nebentaetigkeit));
      fd.append('Punkte', String(this.punkte));

      
      this.nachweise.forEach(f => fd.append('nachweise', f));

      try {
        const res = await fetch('http://localhost:8000/praesentation/antrag', {
          method: 'POST',
          body: fd
        });
        const txt = await res.text().catch(() => '');
        if (!res.ok) throw new Error(txt || 'Fehler beim Senden des Antrags');

        
        this.$router.push('/danke');

      } catch (err) {
        this.fehler = err.message || 'Unbekannter Fehler';
      }
    }
  }
};
</script>

<style scoped>
.form-container{ max-width:700px; margin:auto; padding:25px; background:#ffffff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,.08); }
.form-group{ margin-bottom:15px; }
.form-group label{ font-weight:bold; display:block; margin-bottom:5px; }

input:not([type="checkbox"]):not([type="radio"]), select, textarea{
  width:100%; padding:8px; font-size:14px;
}
textarea{ min-height:70px; }
input[type="checkbox"], input[type="radio"]{ width:auto; margin-right:8px; vertical-align:middle; }

.inline-options{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; }
.inline-options .oder{ opacity:.7; }
.chip{ display:inline-flex; align-items:center; gap:8px; background:#fff; border:1px solid #e5e7eb; border-radius:999px; padding:6px 10px; }
.chip-pts{ background:#eef2ff; border:1px solid #dbe1ff; padding:2px 6px; border-radius:999px; font-weight:600; }

.format-card{ border:1px solid #e5e7eb; border-radius:8px; margin:8px 0; overflow:hidden; background:#fff; }
.format-header{ display:grid; grid-template-columns:1fr 60px; align-items:center; padding:10px 12px; border-bottom:1px solid #e5e7eb; gap:12px; }
.format-table{ display:block; }
.format-table .row{
  display:grid; grid-template-columns:1fr 60px; gap:12px;
  align-items:flex-start; padding:8px 12px; border-bottom:1px solid #f1f3f5;
}
.format-table .row:last-child{ border-bottom:0; }
.pts{ text-align:right; font-weight:600; }


.info-box{ background:#f7fbff; border:1px solid #dbe8ff; border-radius:8px; padding:12px 14px; margin:0 0 16px; }
.hint-box{ background:#f5f7ff; border:1px solid #dbe1ff; border-radius:8px; padding:12px 14px; margin:16px 0 0; }

button{ margin-top:20px; background:#2e7d32; color:#fff; padding:10px 16px; border:none; border-radius:6px; font-size:16px; cursor:pointer; }
.error{ color:#c62828; font-weight:bold; margin-top:10px; }
</style>

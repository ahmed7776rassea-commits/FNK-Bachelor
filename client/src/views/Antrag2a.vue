<template>
  <div class="form-container">
    <h2>Antragsart 2a: Veröffentlichungen (max. 4 Punkte pro Veröffentlichung)</h2>


    <div class="info-box">
      <p>
        <strong>Antragsart 2a:</strong> Lehrabminderung für wissenschaftliche Veröffentlichungen,
        die an der HTW Berlin angefertigt wurden (Affiliation erkennbar), deren Erscheinen zum
        Stichtag <b>15.03.</b> bzw. <b>15.09.</b> nicht länger als <b>12 Monate</b> zurückliegt und
        die inhaltlich begutachtet wurden.
      </p>
      <p>
        Bitte erstellen Sie je Veröffentlichung ein PDF und binden die erforderlichen Nachweise darin ein.
        Bitte beachten Sie die Bearbeitungshinweise.
      </p>
    </div>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Name des/der Antragstellers/in:</label>
        <input v-model="name" required readonly />
      </div>

      <div class="form-group">
        <label>Fachbereich:</label>
        <input v-model="fachbereich" required />
      </div>

      <div class="form-group">
        <label>Titel der Veröffentlichung:</label>
        <input v-model="titel" required />
      </div>

      <div class="form-group">
        <label>Bibliographische Angaben:</label>
        <textarea v-model="biblioAngaben" required></textarea>
      </div>

      <div class="form-group">
        <label>Erscheinungsdatum (online oder print):</label>
        <input type="date" v-model="erscheinung" required />
      </div>

      <div class="form-group">
        <label>Alleinautorenschaft oder Koautorschaft:</label>
        <select v-model="autorenschaft" required>
          <option disabled value="">Bitte auswählen…</option>
          <option value="allein">Alleinautorenschaft (2 Punkte)</option>
          <option value="ko">Koautorschaft (1 Punkt)</option>
        </select>
      </div>

      <div class="form-group">
        <label>Begutachtung:</label>
        <select v-model="begutachtung" required>
          <option disabled value="">Bitte auswählen…</option>
          <option value="peer">Peer Review (2 Punkte)</option>
          <option value="inhaltlich">Inhaltliche Begutachtung durch Dritte (0,5 Punkte) (z.B. Herausgeber, Redaktion; nicht: Lektorat)</option>
        </select>
      </div>

      <div class="hint-box">
        <strong>Hinweise zur inhaltlichen Begutachtung:</strong>
        <ul>
          <li>Nachweis muss von <em>Dritten</em> stammen und für fachfremde Gutachtende nachvollziehbar sein.</li>
          <li>Beispiele: Calls mit Reviewbeschreibung, Autorenhinweise referierter Zeitschriften, Links, Auszüge aus Gutachten, Korrespondenz.</li>
          <li><b>Links müssen funktionieren</b> (keine reinen Scans ohne anklickbare Links).</li>
          <li>Nachweise bitte <b>in das PDF einbinden</b> (keine zusätzliche Datei schicken).</li>
        </ul>
      </div>

      <div class="form-group compact">
        <label>Punkte (automatisch):</label>
        <input :value="punkte" readonly />
      </div>

      <div class="form-group">
        <label>
          <input type="checkbox" v-model="keineEinnahmen" required />
          Hiermit bestätige ich, dass mit dieser Publikation keine Einnahmen aus Nebentätigkeiten verbunden sind.
        </label>
      </div>

      <div class="form-group">
        <label>Nachweise (PDFs einbinden):</label>
        <input type="file" multiple accept="application/pdf" @change="handleFiles" required />
      </div>

      <div v-if="fehler" class="error">{{ fehler }}</div>
      <button type="submit">Absenden</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AntragZweiAForm',
  data() {
    return {
      name: '',
      fachbereich: '',
      titel: '',
      biblioAngaben: '',
      erscheinung: '',
      autorenschaft: '',
      begutachtung: '',
      keineEinnahmen: false,
      nachweise: [],     
      benutzerId: '',
      fehler: ''
    };
  },
  computed: {
    punkte() {
      const autor = this.autorenschaft === 'allein' ? 2 : this.autorenschaft === 'ko' ? 1 : 0;
      const gut   = this.begutachtung === 'peer' ? 2 : this.begutachtung === 'inhaltlich' ? 0.5 : 0;
      const sum   = autor + gut;
      return sum > 4 ? 4 : sum;
    }
  },
  mounted() {
    const userData = JSON.parse(localStorage.getItem("user") || '{}');
    this.name = `${userData.name || ''} ${userData.nachname || ''}`.trim();
    this.fachbereich = userData.fachbereich || userData.studiengang || '';
    this.benutzerId = localStorage.getItem("userId") || '';
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
      if (!this.nachweise.length) {
        this.fehler = 'Bitte laden Sie mindestens ein PDF hoch.';
        return;
      }
      const formData = new FormData();
      formData.append('Benutzer_id', this.benutzerId);
      formData.append('Antragsteller_name', this.name);
      formData.append('Fachbereich', this.fachbereich);
      formData.append('Ermaessigung_SWS', String(0));
      formData.append('Titel_veroeffentlichung', this.titel);
      formData.append('Alleinautor', String(this.autorenschaft === 'allein'));
      formData.append('Koautor', String(this.autorenschaft === 'ko'));
      formData.append('Bibliographische_angaben', this.biblioAngaben);
      formData.append('Erscheinungsdatum', this.erscheinung);
      formData.append('Peer_Review', String(this.begutachtung === 'peer'));
      formData.append('Drittbegutachtung', String(this.begutachtung === 'inhaltlich'));
      formData.append('Einnahmen_nebentaetigkeit', String(this.keineEinnahmen));

     
      this.nachweise.forEach(f => formData.append('nachweise', f));

      try {
        const res = await fetch("http://localhost:8000/veroeffentlichung/antrag", {
          method: "POST",
          body: formData
        });
        const txt = await res.text().catch(() => '');
        if (!res.ok) throw new Error(txt || 'Fehler beim Senden');

        this.$router.push('/danke');
      } catch (err) {
        this.fehler = err?.message || 'Unbekannter Fehler';
      }
    }
  }
};
</script>

<style scoped>
.form-container{ max-width:700px; margin:auto; padding:25px; background:#ffffff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,.08); }
.form-group{ margin-bottom:15px; }
label{ font-weight:bold; display:block; margin-bottom:5px; }
input:not([type="checkbox"]), select, textarea{ width:100%; padding:8px; font-size:14px; }
input[type="checkbox"]{ width:auto; display:inline-block; margin-right:8px; vertical-align:middle; }
button{ margin-top:20px; background:#2e7d32; color:#fff; padding:10px 16px; border:none; border-radius:6px; font-size:16px; cursor:pointer; }
.error{ color:#c62828; font-weight:bold; margin-top:10px; }


.info-box{ background:#f7fbff; border:1px solid #dbe8ff; border-radius:8px; padding:12px 14px; margin:0 0 16px; font-size:14px; }


.hint-box{ background:#f5f7ff; border:1px solid #dbe1ff; border-radius:8px; padding:12px 14px; margin:10px 0 16px; font-size:14px; }
</style>

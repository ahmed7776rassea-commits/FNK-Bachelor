<template>
  <div class="form-container">
    <h2>Drittmittelfinanziertes Vorhaben</h2>
    <div class="info-box">
      <p>
        <strong>Antragsart 1:</strong> Ermäßigung von Lehrdeputaten für die Durchführung bewilligter
        drittmittelfinanzierter Forschungs- und künstlerischer Projekte (außer IFAF und
        gegenfinanzierte Abminderung), deren Abschluss bis zum Stichtag der Antragstellung nicht
        länger als 12 Monate zurückliegt.
      </p>
      <p>
        Bitte erstellen Sie je Projekt ein PDF und binden die erforderlichen Nachweise darin ein.<br />
        <em>Ausnahme:</em> Kleinere Projekte, die jeweils unter der 10.000 €-Grenze liegen, werden
        in einem PDF kumuliert.<br />
        Bitte beachten Sie die Bearbeitungshinweise.
      </p>
    </div>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Name des/der Antragstellers/in:</label>
        <input v-model="name" readonly />
      </div>

      <div class="form-group">
        <label>Fachbereich:</label>
        <input v-model="fachbereich" required />
      </div>

      <div class="form-group">
        <label>Titel des Vorhabens:</label>
        <input v-model="titel" required />
      </div>

      <div class="form-group">
        <label>Dauer des Vorhabens:</label>
        <div class="date-group">
          <input type="date" v-model="von" required />
          <span>bis</span>
          <input type="date" v-model="bis" required />
        </div>
      </div>

      <div class="form-group">
        <label>Drittmittelgeber:</label>
        <input v-model="mittelgeber" required />
      </div>

      <div class="form-group">
        <label>Höhe der Drittmittel für das Projekt über die Gesamtlaufzeit (nur Anteil der HTW Berlin):</label>
        <input type="number" v-model.number="gesamtmittel" required />
      </div>

      <div class="form-group">
        <label>Höhe der dem/der Antragssteller/in zugeordneten Drittmittel für das Projekt über die Gesamtlaufzeit</label>
        <input type="number" v-model.number="zugewiesen" required />
      </div>

      <div class="form-group">
        <label>Höhe der zum Zeitpunkt der Antragstellung für den Einsatz zur Lehrabminderung noch verfügbaren Mittel:</label>
        <input type="number" v-model.number="verfuegbar" required />
      </div>

      <div class="form-group">
        <label>Höhe der hiervon für den Antragszeitraum (Semester) zur Lehrabminderung eingesetzten Mittel :</label>
        <input type="number" v-model.number="eingesetzt" required />
      </div>

      <div class="points-wrap">
        <label class="points-label">Höhe der eingesetzten Drittmittel pro Semester in €</label>

        <table class="points-table">
          <thead>
            <tr><th>Betrag (≥)</th><th>Punkte</th></tr>
          </thead>
          <tbody>
            <tr :class="{ active: punkte === 1 }"><td>10.000</td><td>1</td></tr>
            <tr :class="{ active: punkte === 2 }"><td>20.000</td><td>2</td></tr>
            <tr :class="{ active: punkte === 3 }"><td>30.000</td><td>3</td></tr>
            <tr :class="{ active: punkte === 4 }"><td>40.000</td><td>4</td></tr>
            <tr :class="{ active: punkte === 5 }"><td>50.000</td><td>5</td></tr>
          </tbody>
        </table>

        <div class="form-group compact">
          <label>Punkte (automatisch):</label>
          <input :value="punkte" readonly />
        </div>
      </div>

      <div class="form-group">
        <label>
          <input type="checkbox" v-model="nebentaetigkeit" />
          Hiermit bestätige ich, dass mit diesem Vorhaben keine Einnahmen aus Nebentätigkeiten
          verbunden sind.
        </label>
      </div>

      <div class="form-group">
        <label>
          <input type="checkbox" v-model="zulage" />
          Hiermit bestätige ich, dass mit diesem Vorhaben keine Zahlung einer Forschungszulage
          verbunden ist und keine Lehrabminderung nach § 9 Abs. 6 LVVO (gegenfinanzierte Abminderung,
          Forschungsprofessur) in Anspruch genommen wird.
        </label>
      </div>

      <div class="form-group">
        <label>Nachweise (PDFs einbinden):</label>
        <input type="file" multiple accept="application/pdf" @change="handleFiles" />
      </div>

      <div class="footnotes">
        <p>
          Der betreffende Ausschnitt aus dem Nachweis vom Mittelgeber (z. B.
          Zuwendungsbescheid / Auftrag / Vertrag) ist in dieses PDF einzubinden (keine zusätzliche
          Datei schicken).
        </p>
        <p> Ein von allen beteiligten hier Antragsberechtigten unterschriebenes Dokument</p>
      </div>

      <div v-if="fehler" class="error">{{fehler}}</div>
      <button type="submit">Absenden</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Antrag1Form',
  data() {
    return {
      name: '',
      fachbereich: '',
      benutzerId: '',
      titel: '',
      von: '',
      bis: '',
      mittelgeber: '',
      gesamtmittel: null,
      zugewiesen: null,
      verfuegbar: null,
      eingesetzt: null,
      nebentaetigkeit: false,
      zulage: false,
      nachweise: [],       
      fehler: ''
    };
  },
  computed: {
    punkte() {
      const v = Number(this.eingesetzt) || 0;
      if (v >= 50000) return 5;
      if (v >= 40000) return 4;
      if (v >= 30000) return 3;
      if (v >= 20000) return 2;
      if (v >= 10000) return 1;
      return 0;
    }
  },
  mounted() {
    const userData = localStorage.getItem('user');
    const userId = localStorage.getItem('userId');
    if (userData && userId) {
      const parsed = JSON.parse(userData);
      this.name = `${parsed.name} ${parsed.nachname}`;
      this.fachbereich = parsed.studiengang || '';
      this.benutzerId = userId;
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

      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('Benutzer_id', this.benutzerId);
      formData.append('fachbereich', this.fachbereich);
      formData.append('titel', this.titel);
      formData.append('von', this.von);
      formData.append('bis', this.bis);
      formData.append('mittelgeber', this.mittelgeber);
      formData.append('gesamt_htw', String(this.gesamtmittel ?? ''));
      formData.append('zugeordnet_antragsteller', String(this.zugewiesen ?? ''));
      formData.append('verfuegbar_zum_antragszeitpunkt', String(this.verfuegbar ?? ''));
      formData.append('eingesetzt_im_semester', String(this.eingesetzt ?? ''));
      formData.append('punkte', String(this.punkte));
      formData.append('nebentaetigkeit', String(this.nebentaetigkeit));
      formData.append('zulage', String(this.zulage));

      
      this.nachweise.forEach(file => {
        formData.append('nachweise', file);
      });

      try {
        const res = await fetch('http://localhost:8000/drittmittel/antrag', {
          method: 'POST',
          body: formData
        });
        const txt = await res.text().catch(() => '');
        if (!res.ok) throw new Error(txt || `Fehler beim Senden (HTTP ${res.status})`);

        this.$router.push('/danke');
      } catch (err) {
        this.fehler = err?.message || 'Unbekannter Fehler';
      }
    }
  }
};
</script>

<style scoped>
.form-container { max-width: 700px; margin: auto; padding: 25px; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.08); }
.form-group { margin-bottom: 15px; }
.form-group.compact { margin-top: 10px; }
.form-group label { font-weight: bold; display: block; margin-bottom: 5px; }
input { width: 100%; padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 6px; }
input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
input[type="number"] { -moz-appearance: textfield; appearance: textfield; }
.date-group { display: flex; gap: 10px; align-items: center; }
input[type="checkbox"] { width: auto; margin-right: 8px; }
.points-wrap { margin: 20px 0 10px; }
.points-label { display: block; font-weight: bold; margin-bottom: 8px; }
.points-table { width: 100%; border-collapse: collapse; margin-bottom: 8px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }
.points-table th, .points-table td { padding: 10px 12px; border-bottom: 1px solid #e5e7eb; text-align: left; }
.points-table thead th { background: #eef2f7; font-weight: 700; }
.points-table tr.active { background: #eaffef; font-weight: 700; }
.info-box{ background:#f7fbff; border:1px solid #dbe8ff; border-radius:8px; padding:12px 14px; margin:0 0 16px; font-size:14px; }
.footnotes{ background:#f9f9f9; border:1px dashed #cfcfcf; border-radius:8px; padding:10px 12px; margin:6px 0 14px; font-size:13px; }
button { margin-top: 20px; background: #2e7d32; color: white; padding: 10px 16px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
.error { color: #c62828; font-weight: bold; margin-top: 10px; }
</style>

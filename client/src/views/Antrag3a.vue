<template>
  <div class="form-container">
    <h2>Antragsart 3a: Betreuung von Promotionen (einmalig 1 SWS)</h2>

    
    <div class="info-box">
      <p>
        <strong>Antragsart 3a:</strong> Ermäßigung von Lehrdeputaten für die Betreuung von Promotionen
        (außerhalb von Promotionszentren, in Kooperation mit einer externen promotionsberechtigten Einrichtung).
        Gefördert werden Vorhaben, deren <b>Beginn</b> bis zum Stichtag <b>15.03.</b> bzw. <b>15.09.</b> nicht
        länger als <b>12 Monate</b> zurückliegt.
      </p>
      <p>
        Bitte erstellen Sie je Vorhaben <b>ein PDF</b> und binden die erforderlichen Nachweise darin ein.
        Bitte beachten Sie die <b>Bearbeitungshinweise</b>.
      </p>
    </div>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Beteiligte Universität:</label>
        <input v-model="uni" required />
      </div>

      <div class="form-group">
        <label>Name des Promovenden/der Promovendin:</label>
        <input v-model="promovend_name" required />
      </div>

      <div class="form-group">
        <label>Arbeitstitel der Dissertation:</label>
        <input v-model="arbeitstitel" required />
      </div>

      <div class="form-group">
        <label>Datum des Beginns lt. Betreuungsvereinbarung:</label>
        <input type="date" v-model="beginn_betreuung" required />
      </div>

      <div class="form-group">
        <label>Voraussichtl. Dauer des Promotionsvorhabens:</label>
        <div class="date-group">
          <input type="date" v-model="dauer_von" required />
          <span>von</span>
          <span>bis</span>
          <input type="date" v-model="dauer_bis" required />
        </div>
      </div>

      <div class="form-group">
        <label class="inline-check">
          <input type="checkbox" v-model="keineEinnahmen" required />
          Hiermit bestätige ich, dass mit dieser Dissertation keine Einnahmen aus Nebentätigkeiten verbunden sind.
        </label>
      </div>

      <div class="form-group">
        <label>Nachweis (PDF einbinden):</label>
        <input type="file" @change="handleFile" accept="application/pdf" required />
      </div>

      <div class="hint-box">
        <p>
          * Die Betreuung durch den/die Antragsteller/in ist in geeigneter Form
          <b>in dieses PDF</b> (z.&nbsp;B. Betreuungsvereinbarung) einzubinden
          – keine zusätzliche Datei schicken.
        </p>
      </div>

      <div v-if="fehler" class="error">{{ fehler }}</div>
      <button type="submit">Absenden</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Antrag3aPromotionForm',
  data() {
    return {
      benutzer_id: '',
      antragsteller_name: '',
      beginn_promotion: '',
      uni: '',
      promovend_name: '',
      arbeitstitel: '',
      beginn_betreuung: '',
      dauer_von: '',
      dauer_bis: '',
      keineEinnahmen: false,
      nachweis: null,
      fehler: ''
    };
  },
  mounted() {
    const userData = localStorage.getItem("user");
    const userId = localStorage.getItem("userId");
    if (userData && userId) {
      const parsed = JSON.parse(userData);
      this.benutzer_id = userId;
      this.antragsteller_name = `${parsed.name || ''} ${parsed.nachname || ''}`.trim();
      this.fachbereich = parsed.fachbereich || parsed.studiengang || '';
    }
  },
  methods: {
    handleFile(e) {
      const f = e.target.files[0];
      if (!f) { this.nachweis = null; return; }
      if (f.type !== 'application/pdf') {
        this.fehler = 'Bitte nur PDF-Dateien hochladen.';
        e.target.value = '';
        return;
      }
      this.nachweis = f;
    },
    async submitForm() {
      this.fehler = '';
      if (!this.nachweis) {
        this.fehler = 'Bitte laden Sie den Nachweis (PDF) hoch.';
        return;
      }

      const fd = new FormData();
      fd.append("Benutzer_id", this.benutzer_id);
      fd.append("Antragsteller_name", this.antragsteller_name);
      fd.append("Beteiligte_Universitaet", this.uni);
      fd.append("Promovend_name", this.promovend_name);
      fd.append("Arbeitstitel", this.arbeitstitel);
      fd.append("Beginn_Betreuung", this.beginn_betreuung);
      fd.append("Zeitraum_von", this.dauer_von);
      fd.append("Zeitraum_bis", this.dauer_bis);
      fd.append("Einnahmen_nebentaetigkeit", String(this.keineEinnahmen));
      fd.append("nachweis", this.nachweis);

      try {
        const res = await fetch("http://localhost:8000/promotionen/antrag", {
          method: "POST",
          body: fd
        });
        const txt = await res.text().catch(() => '');
        if (!res.ok) throw new Error(txt || "Fehler beim Senden des Antrags");
        this.$router.push('/danke');
      } catch (err) {
        this.fehler = err.message || 'Unbekannter Fehler';
      }
    }
  }
};
</script>

<style scoped>
.form-container{
  max-width:700px;
  margin:auto;
  padding:25px;
  background:#f9f9f9;
  border-radius:12px;
}
.form-group{ margin-bottom:15px; }
.form-group label:not(.inline-check){
  font-weight:bold;
  display:block;
  margin-bottom:5px;
}
input:not([type="checkbox"]):not([type="radio"]),
textarea,
select{
  width:100%;
  padding:8px;
  font-size:14px;
}
.date-group{
  display:flex;
  gap:10px;
  align-items:center;
}
.form-group label.inline-check{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:normal;   
  margin-bottom:0;      
}
.form-group label.inline-check input[type="checkbox"]{
  margin:0;
}
button{
  margin-top:20px;
  background:#2e7d32;
  color:#fff;
  padding:10px 16px;
  border:none;
  border-radius:6px;
  font-size:16px;
  cursor:pointer;
}
.info-box{
  background:#f7fbff;
  border:1px solid #dbe8ff;
  border-radius:8px;
  padding:12px 14px;
  margin:0 0 16px;
  font-size:14px;
}
.hint-box{
  background:#f5f7ff;
  border:1px solid #dbe1ff;
  border-radius:8px;
  padding:12px 14px;
  margin:16px 0 0;
  font-size:14px;
}
.error{
  color:#c62828;
  font-weight:bold;
  margin-top:10px;
}
</style>


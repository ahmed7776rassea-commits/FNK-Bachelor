<template>
  <div class="page">
    <section class="card">
      <header class="card__header">
        <h1 class="card__title">Vor dem Antrag</h1>
        <p class="card__sub">Bitte lesen und bestätigen Sie die Hinweise, bevor Sie fortfahren.</p>
      </header>

      <div class="divider"></div>

      <article class="content">
        <h2>Hinweise Wichtige Informationen</h2>

        <section class="block">
          <h3>Kontingent</h3>
          <ul>
            <li>Gesamtuniversitäres Kontingent: <strong>120 SWS</strong>.</li>
            <li>Empfehlung der FNK: max. <strong>4 SWS</strong> pro Person und Semester.</li>
          </ul>
        </section>

        <section class="block">
          <h3>Antragsarten</h3>
          <ol>
            <li><strong>Antrag 1:</strong> Drittmittelfinanzierte Forschungs- oder künstlerische Projekte. Kleinere Projekte (&lt; 10.000 €) können in einem Antrag kumuliert werden.</li>
            <li><strong>Antrag 2a:</strong> Wissenschaftliche Veröffentlichungen (Full Paper/Monographie) mit nachvollziehbarer inhaltlicher Begutachtung (z. B. Peer Review).</li>
            <li><strong>Antrag 2b:</strong> Künstlerische Präsentationen/Publikationen (z. B. auf Einladung, nach Juryentscheidung oder im Wettbewerb) mit geeigneten Nachweisen.</li>
            <li><strong>Antrag 3a:</strong> Betreuung eines Promotionsvorhabens, das in den letzten 12 Monaten begonnen hat.</li>
            <li><strong>Antrag 3b:</strong> Betreuung eines Promotionsvorhabens, das in den letzten 12 Monaten abgeschlossen wurde.</li>
          </ol>
        </section>

        <section class="block">
          <h3>Ausschlüsse</h3>
          <ul>
            <li>IFAF-Projekte (separates Kontingent).</li>
            <li>Bereits nach § 9 Abs. 6 LVVO gegenfinanzierte Lehrabminderung / Forschungsprofessur.</li>
            <li>Reine Lehr-/Transfervorhaben ohne Forschungscharakter.</li>
            <li>Vorhaben mit Forschungszulage oder vergüteter Nebentätigkeit (§ 6 Abs. 1 NtV).</li>
          </ul>
        </section>

        <section class="block">
          <h3>Nachweise (Beispiele)</h3>
          <ul>
            <li>Calls for Papers mit Beschreibung des Review-Prozesses, Richtlinien referierter Zeitschriften, Auszüge aus Gutachten, Korrespondenz mit Herausgebenden.</li>
            <li>Bei künstlerischen Vorhaben: Juryentscheidung/Einladung, veröffentlichte Ankündigung, aussagekräftiger Auszug aus der medialen Berichterstattung.</li>
            <li>Wenn Peer-Review im Fach unüblich ist: kurze Erläuterung + geeignete Qualitätssicherung.</li>
          </ul>
        </section>

        <section class="block">
          <h3>Bearbeitungshinweise</h3>
          <ul>
            <li>Pro Projekt / Publikation / Promotion ein <strong>separates Antragsformular</strong>.</li>
            <li>Alle Nachweise in <strong>ein</strong> PDF integrieren; eingebettete Links müssen funktionieren. Keine gescannten Formulare, keine Belegexemplare, kein Anschreiben.</li>
            <li>Nachweis des Forschungscharakters bei Drittmittelgebern/Programmen wie z. B. DAAD, Stiftung Innovation in der Hochschullehre, Erasmus, EXIST.</li>
            <li>Digitale Einreichung über die Webseite bzw. per HTW-E-Mail an das Dekanat (Cc: VP Forschung). Versand von HTW-E-Mail ersetzt die Unterschrift.</li>
          </ul>
        </section>

        <details class="details">
          <summary>Weitere Details anzeigen</summary>
          <p>
            Für Antrag&nbsp;1 können Mittel nach Bedarf semesterweise eingesetzt werden, bis die Gesamtsumme aus dem Zuwendungsbescheid ausgeschöpft ist. Bei Antrag&nbsp;2a zählen nur <em>inhaltlich begutachtete</em> Beiträge (keine Abstracts, Poster, Lehrbücher, Herausgeberschaften, Eigenverlag). Bei Antrag&nbsp;3 ist die Betreuung (und bei 3b zusätzlich der Abschluss) in geeigneter Form nachzuweisen, z. B. Betreuungsvereinbarung / Link zur veröffentlichten Dissertation.
          </p>
        </details>

        <label class="confirm">
          <input type="checkbox" v-model="ack" />
          <span>Ich habe die Hinweise gelesen und verstanden.</span>
        </label>

        <button class="btn btn--green" :disabled="!ack" @click="handleWeiter">
          Weiter
        </button>
      </article>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HinweisePage',
  data() {
    return {
      ack: false,
    }
  },
  methods: {
    handleWeiter() {
      if (this.ack) {
        this.$router.push('/funktionen')
      }
    },
  },
}
</script>

<style scoped>
:host, .page {
  font-family: Arial, sans-serif;
  background-color: #f6f7fb;
  min-height: 100vh;
  display: grid;
  place-items: start center;
  padding: 40px 16px;
}

.card {
  width: 100%;
  max-width: 840px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,.08);
  padding: 28px;
}

.card__header { margin-bottom: 12px; }
.card__title {
  margin: 0 0 6px 0;
  font-size: 26px;
  color: #0f172a;
  font-weight: 700;
  line-height: 1.25;
}
.card__sub {
  margin: 0;
  color: #475569;
  font-size: 15px;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 18px 0 10px 0;
}

.content {
  color: #0f172a;
  line-height: 1.75;
  font-size: 15.5px;
}

h2 {
  margin: 0 0 14px 0;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: .2px;
}

h3 {
  margin: 18px 0 8px 0;
  font-size: 16.5px;
  font-weight: 700;
}

.block { margin-bottom: 14px; }

ul, ol {
  margin: 0;
  padding-left: 22px;
}
ul li, ol li {
  margin-bottom: 6px;
}

.details {
  margin: 6px 0 16px 0;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
}
.details summary {
  cursor: pointer;
  font-weight: 600;
  color: #0284c7;
  outline: none;
}
.details p { margin: 8px 0 0 0; }

.confirm {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 6px 0 14px 0;
  user-select: none;
}
.confirm input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 160px;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: transform .06s ease, box-shadow .12s ease, opacity .12s ease;
}
.btn--green {
  background: #16a34a;
  color: #fff;
  box-shadow: 0 2px 10px rgba(22,163,74,.25);
}
.btn--green:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(22,163,74,.35);
}
.btn--green:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(22,163,74,.25);
}
.btn:disabled {
  opacity: .55;
  cursor: not-allowed;
}

@media (max-width: 560px) {
  .card { padding: 20px; }
  .card__title { font-size: 22px; }
  h2 { font-size: 18px; }
}
</style>

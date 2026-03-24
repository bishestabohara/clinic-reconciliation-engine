const sampleQualityPayload = {
  demographics: { name: 'John Doe', dob: '1955-03-15', gender: 'M' },
  medications: ['Metformin 500mg', 'Lisinopril 10mg'],
  allergies: [],
  conditions: ['Type 2 Diabetes'],
  vital_signs: { blood_pressure: '340/180', heart_rate: 72 },
  last_updated: '2024-06-15',
}

function QualityForm({ value, onChange, onSubmit, isLoading }) {
  return (
    <section className="rounded-[28px] border border-slate-200 bg-white/90 p-6 shadow-[0_24px_70px_-30px_rgba(20,55,48,0.45)]">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="m-0 text-sm font-semibold uppercase tracking-[0.22em] text-sky-700">
            Data Quality Validation
          </p>
          <h2 className="mt-2 m-0 text-2xl font-semibold tracking-tight text-slate-900">
            Score record completeness and plausibility
          </h2>
        </div>
        <button
          type="button"
          className="rounded-full border border-sky-200 px-4 py-2 text-sm font-semibold text-sky-700"
          onClick={() => onChange(JSON.stringify(sampleQualityPayload, null, 2))}
        >
          Load sample
        </button>
      </div>

      <p className="mt-4 m-0 text-sm leading-6 text-slate-600">
        Paste or edit a patient record payload in JSON format to score data quality and flag
        incomplete or implausible fields.
      </p>

      <textarea
        className="mt-5 min-h-80 w-full rounded-2xl border border-slate-200 bg-slate-950 p-4 font-mono text-sm leading-6 text-slate-100 outline-none ring-0"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />

      <button
        type="button"
        onClick={onSubmit}
        disabled={isLoading}
        className="mt-4 rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white disabled:opacity-60"
      >
        {isLoading ? 'Validating...' : 'Run validation'}
      </button>
    </section>
  )
}

export default QualityForm

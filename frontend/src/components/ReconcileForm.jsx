const sampleMedicationPayload = {
  patient_context: {
    age: 67,
    conditions: ['Type 2 Diabetes', 'Hypertension'],
    recent_labs: { eGFR: 45 },
  },
  sources: [
    {
      system: 'Hospital EHR',
      medication: 'Metformin 1000mg twice daily',
      last_updated: '2024-10-15',
      source_reliability: 'high',
    },
    {
      system: 'Primary Care',
      medication: 'Metformin 500mg twice daily',
      last_updated: '2025-01-20',
      source_reliability: 'high',
    },
    {
      system: 'Pharmacy',
      medication: 'Metformin 1000mg daily',
      last_filled: '2025-01-25',
      source_reliability: 'medium',
    },
  ],
}

function ReconcileForm({ value, onChange, onSubmit, isLoading }) {
  return (
    <section className="rounded-[28px] border border-slate-200 bg-white/90 p-6 shadow-[0_24px_70px_-30px_rgba(20,55,48,0.45)]">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="m-0 text-sm font-semibold uppercase tracking-[0.22em] text-emerald-700">
            Medication Reconciliation
          </p>
          <h2 className="mt-2 m-0 text-2xl font-semibold tracking-tight text-slate-900">
            Compare conflicting medication sources
          </h2>
        </div>
        <button
          type="button"
          className="rounded-full border border-emerald-200 px-4 py-2 text-sm font-semibold text-emerald-700"
          onClick={() => onChange(JSON.stringify(sampleMedicationPayload, null, 2))}
        >
          Load sample
        </button>
      </div>

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
        {isLoading ? 'Reconciling...' : 'Run reconciliation'}
      </button>
    </section>
  )
}

export default ReconcileForm

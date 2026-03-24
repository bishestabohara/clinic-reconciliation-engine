import { useState } from 'react'

import QualityForm from '../components/QualityForm'
import ReconcileForm from '../components/ReconcileForm'
import ResultCard from '../components/ResultCard'
import ScoreBadge from '../components/ScoreBadge'
import { reconcileMedication, validateDataQuality } from '../lib/api'

const medicationSample = `{
  "patient_context": {
    "age": 67,
    "conditions": ["Type 2 Diabetes", "Hypertension"],
    "recent_labs": { "eGFR": 45 }
  },
  "sources": [
    {
      "system": "Hospital EHR",
      "medication": "Metformin 1000mg twice daily",
      "last_updated": "2024-10-15",
      "source_reliability": "high"
    },
    {
      "system": "Primary Care",
      "medication": "Metformin 500mg twice daily",
      "last_updated": "2025-01-20",
      "source_reliability": "high"
    }
  ]
}`

const qualitySample = `{
  "demographics": { "name": "John Doe", "dob": "1955-03-15", "gender": "M" },
  "medications": ["Metformin 500mg", "Lisinopril 10mg"],
  "allergies": [],
  "conditions": ["Type 2 Diabetes"],
  "vital_signs": { "blood_pressure": "340/180", "heart_rate": 72 },
  "last_updated": "2024-06-15"
}`

function Dashboard() {
  const [medicationPayload, setMedicationPayload] = useState(medicationSample)
  const [qualityPayload, setQualityPayload] = useState(qualitySample)
  const [reconcileResult, setReconcileResult] = useState(null)
  const [qualityResult, setQualityResult] = useState(null)
  const [decision, setDecision] = useState('Pending review')
  const [error, setError] = useState('')
  const [loadingSection, setLoadingSection] = useState('')

  const qualityIssues =
    qualityResult?.issues_detected?.filter((issue) => issue.field !== 'summary') || []
  const qualitySummary =
    qualityResult?.issues_detected?.find((issue) => issue.field === 'summary')?.issue || ''

  async function handleReconcile() {
    setError('')
    setLoadingSection('reconcile')

    try {
      const parsedPayload = JSON.parse(medicationPayload)
      const data = await reconcileMedication(parsedPayload)
      setReconcileResult(data)
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'Unable to reconcile medication.')
    } finally {
      setLoadingSection('')
    }
  }

  async function handleQualityCheck() {
    setError('')
    setLoadingSection('quality')

    try {
      const parsedPayload = JSON.parse(qualityPayload)
      const data = await validateDataQuality(parsedPayload)
      setQualityResult(data)
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'Unable to validate data quality.')
    } finally {
      setLoadingSection('')
    }
  }

  return (
    <main className="min-h-screen px-4 py-8 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <section className="rounded-[36px] border border-white/70 bg-[linear-gradient(135deg,rgba(13,47,54,0.95),rgba(25,91,86,0.88))] px-6 py-10 text-white shadow-[0_35px_90px_-45px_rgba(10,35,42,0.75)] sm:px-10">
          <p className="m-0 text-sm font-semibold uppercase tracking-[0.28em] text-emerald-200">
            Clinical Review Workspace
          </p>
          <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
            Clinical Data Reconciliation Engine
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-emerald-50/90 sm:text-lg">
            A clinician-friendly dashboard for resolving conflicting medication data and surfacing
            patient record quality risks.
          </p>
        </section>

        {error ? (
          <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {error}
          </div>
        ) : null}

        <section className="mt-8 grid gap-6 xl:grid-cols-2">
          <ReconcileForm
            value={medicationPayload}
            onChange={setMedicationPayload}
            onSubmit={handleReconcile}
            isLoading={loadingSection === 'reconcile'}
          />
          <QualityForm
            value={qualityPayload}
            onChange={setQualityPayload}
            onSubmit={handleQualityCheck}
            isLoading={loadingSection === 'quality'}
          />
        </section>

        <section className="mt-8 grid gap-6 xl:grid-cols-2">
          <ResultCard
            title="Reconciliation Outcome"
            confidence={reconcileResult?.confidence_score}
            safety={reconcileResult?.clinical_safety_check}
            reasoning={reconcileResult?.reasoning}
            actions={reconcileResult?.recommended_actions || []}
          >
            <p className="mt-5 text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
              Most likely active medication
            </p>
            <p className="mt-2 text-2xl font-semibold text-slate-900">
              {reconcileResult?.reconciled_medication || 'Run reconciliation to see a result.'}
            </p>

            <div className="mt-5 flex flex-wrap gap-3">
              <button
                type="button"
                className="rounded-full bg-emerald-600 px-4 py-2 text-sm font-semibold text-white"
                onClick={() => setDecision('Approved')}
              >
                Approve
              </button>
              <button
                type="button"
                className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700"
                onClick={() => setDecision('Rejected')}
              >
                Reject
              </button>
              <ScoreBadge label="Review status" value={decision} tone="slate" />
            </div>
          </ResultCard>

          <ResultCard title="Quality Snapshot" reasoning="">
            <div className="mt-5 flex flex-wrap gap-2">
              <ScoreBadge label="Overall" value={qualityResult?.overall_score ?? '--'} tone="yellow" />
              <ScoreBadge
                label="Completeness"
                value={qualityResult?.breakdown?.completeness ?? '--'}
                tone="green"
              />
              <ScoreBadge
                label="Accuracy"
                value={qualityResult?.breakdown?.accuracy ?? '--'}
                tone="yellow"
              />
              <ScoreBadge
                label="Timeliness"
                value={qualityResult?.breakdown?.timeliness ?? '--'}
                tone="yellow"
              />
              <ScoreBadge
                label="Plausibility"
                value={qualityResult?.breakdown?.clinical_plausibility ?? '--'}
                tone="red"
              />
            </div>

            <div className="mt-5 rounded-2xl border border-slate-200 bg-white p-4">
              <p className="m-0 text-sm font-medium text-slate-900">Quality summary</p>
              <p className="mt-2 m-0 text-sm leading-6 text-slate-700">
                {qualitySummary || 'Run validation to generate a summary of the current quality risks.'}
              </p>
            </div>

            <div className="mt-5 rounded-2xl bg-slate-50 p-4">
              <p className="m-0 text-sm font-medium text-slate-900">Detected issues</p>
              <ul className="mt-3 space-y-3 pl-5 text-sm text-slate-700">
                {qualityIssues.map((issue) => (
                  <li key={`${issue.field}-${issue.issue}`}>
                    <span className="font-semibold text-slate-900">{issue.field}:</span> {issue.issue}
                  </li>
                ))}
                {!qualityIssues.length ? (
                  <li>No issues yet. Run validation to score a record.</li>
                ) : null}
              </ul>
            </div>
          </ResultCard>
        </section>
      </div>
    </main>
  )
}

export default Dashboard

import ScoreBadge from './ScoreBadge'

function ResultCard({ title, confidence, safety, reasoning, actions = [], children }) {
  const confidenceTone = confidence >= 0.8 ? 'green' : confidence >= 0.6 ? 'yellow' : 'red'

  return (
    <section className="rounded-[28px] border border-white/70 bg-white/85 p-6 shadow-[0_24px_70px_-30px_rgba(20,55,48,0.45)] backdrop-blur">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="m-0 text-2xl font-semibold tracking-tight text-slate-900">{title}</h2>
        <div className="flex flex-wrap gap-2">
          {confidence !== undefined ? (
            <ScoreBadge label="Confidence" value={`${Math.round(confidence * 100)}%`} tone={confidenceTone} />
          ) : null}
          {safety ? <ScoreBadge label="Safety" value={safety} tone="yellow" /> : null}
        </div>
      </div>

      {children}

      {reasoning ? (
        <div className="mt-5 rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
          <p className="m-0 font-medium text-slate-900">Reasoning</p>
          <p className="mt-2 m-0">{reasoning}</p>
        </div>
      ) : null}

      {actions.length > 0 ? (
        <div className="mt-5">
          <p className="m-0 text-sm font-medium text-slate-900">Recommended actions</p>
          <ul className="mt-3 space-y-2 pl-5 text-sm text-slate-700">
            {actions.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  )
}

export default ResultCard

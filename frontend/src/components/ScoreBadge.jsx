const toneClasses = {
  green: 'bg-emerald-100 text-emerald-800 ring-emerald-200',
  yellow: 'bg-amber-100 text-amber-800 ring-amber-200',
  red: 'bg-rose-100 text-rose-800 ring-rose-200',
  slate: 'bg-slate-100 text-slate-700 ring-slate-200',
}

function ScoreBadge({ label, value, tone = 'slate' }) {
  return (
    <div className={`rounded-full px-3 py-1 text-sm font-semibold ring-1 ${toneClasses[tone]}`}>
      {label}: {value}
    </div>
  )
}

export default ScoreBadge

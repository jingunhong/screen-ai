import type { Well, WellImage, Plate } from '../types/projects'

interface WellDetailPanelProps {
  well: Well
  plate: Plate
  images: WellImage[]
}

export function WellDetailPanel({ well, plate, images }: WellDetailPanelProps) {
  // Determine QC status badge color and text
  const getQcBadge = () => {
    const score = well.qc_score || 0
    if (score >= 0.8) {
      return {
        bg: 'bg-emerald-100',
        text: 'text-emerald-700',
        border: 'border-emerald-200',
        label: 'Pass',
      }
    } else if (score >= 0.6) {
      return {
        bg: 'bg-amber-100',
        text: 'text-amber-700',
        border: 'border-amber-200',
        label: 'Review',
      }
    } else {
      return {
        bg: 'bg-rose-100',
        text: 'text-rose-700',
        border: 'border-rose-200',
        label: 'Fail',
      }
    }
  }

  const qcBadge = getQcBadge()

  return (
    <aside className="flex-none w-[360px] border-l border-slate-200 dark:border-slate-800 bg-white dark:bg-[#111a22] flex flex-col shadow-2xl z-10">
      {/* Header */}
      <div className="flex items-center justify-between p-5 border-b border-slate-100 dark:border-slate-800">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">data_usage</span>
          Well Metadata
        </h3>
        <span
          className={`px-2 py-0.5 rounded-md ${qcBadge.bg} ${qcBadge.text} text-xs font-bold border ${qcBadge.border}`}
        >
          {well.position} &bull; {qcBadge.label}
        </span>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-0">
        {/* Main Info Grid */}
        <div className="p-5">
          <div className="grid grid-cols-[30%_1fr] gap-y-4 text-sm">
            <div className="text-slate-500 dark:text-slate-400 font-medium">Plate ID</div>
            <div className="text-slate-900 dark:text-white font-semibold">{plate.name}</div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">Cell Line</div>
            <div className="text-slate-900 dark:text-white font-semibold">
              {well.cell_line || 'N/A'}
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">Compound</div>
            <div className="text-slate-900 dark:text-white font-semibold">
              {well.compound_name
                ? `${well.compound_name} (${well.concentration}${well.concentration_unit})`
                : 'N/A'}
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">Incubation</div>
            <div className="text-slate-900 dark:text-white font-semibold">
              {well.incubation_hours ? `${well.incubation_hours} Hours` : 'N/A'}
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">Cell Count</div>
            <div className="text-slate-900 dark:text-white font-semibold">
              {well.cell_count?.toLocaleString() || 'N/A'}
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">Viability</div>
            <div className="text-slate-900 dark:text-white font-semibold flex items-center gap-2">
              {well.viability ? `${Math.round(well.viability * 100)}%` : 'N/A'}
              {well.viability && (
                <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${well.viability >= 0.7 ? 'bg-emerald-500' : well.viability >= 0.5 ? 'bg-amber-500' : 'bg-rose-500'}`}
                    style={{ width: `${well.viability * 100}%` }}
                  ></div>
                </div>
              )}
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-medium">QC Score</div>
            <div className="text-slate-900 dark:text-white font-semibold flex items-center gap-2">
              {well.qc_score?.toFixed(2) || 'N/A'}
              {well.qc_score && (
                <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${well.qc_score >= 0.8 ? 'bg-emerald-500' : well.qc_score >= 0.6 ? 'bg-amber-500' : 'bg-rose-500'}`}
                    style={{ width: `${well.qc_score * 100}%` }}
                  ></div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Separator */}
        <div className="h-px bg-slate-100 dark:bg-slate-800 mx-5"></div>

        {/* Image Previews */}
        <div className="p-5">
          <h4 className="text-sm font-bold text-slate-900 dark:text-white mb-3">
            Field Captures ({images.length})
          </h4>
          <div className="grid grid-cols-2 gap-2">
            {images.map((image) => (
              <div
                key={image.id}
                className="aspect-square rounded-lg bg-slate-100 dark:bg-slate-800 relative overflow-hidden group cursor-pointer border border-slate-200 dark:border-slate-700"
              >
                <div
                  className="w-full h-full bg-center bg-cover"
                  style={{ backgroundImage: `url("${image.thumbnail_url}")` }}
                ></div>
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="material-symbols-outlined text-white">open_in_full</span>
                </div>
                <div className="absolute bottom-1 left-1 px-1.5 py-0.5 bg-black/60 rounded text-[10px] text-white font-medium">
                  {image.channel}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notes Section */}
        {well.analyst_notes && (
          <div className="px-5 pb-5">
            <h4 className="text-sm font-bold text-slate-900 dark:text-white mb-2">Analyst Notes</h4>
            <div className="bg-slate-50 dark:bg-slate-800 p-3 rounded-lg border border-slate-100 dark:border-slate-700">
              <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                {well.analyst_notes}
              </p>
              {well.analyst_name && well.notes_updated_at && (
                <div className="mt-2 text-[10px] text-slate-400 font-medium">
                  Updated {well.notes_updated_at} by {well.analyst_name}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="p-5 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#0c1218]">
        <div className="flex gap-3">
          <button className="flex-1 h-10 rounded-lg bg-primary hover:bg-blue-600 text-white font-bold text-sm shadow-sm transition-colors flex items-center justify-center gap-2">
            <span className="material-symbols-outlined text-[18px]">visibility</span>
            Full View
          </button>
          <button className="flex-1 h-10 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-bold text-sm hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors flex items-center justify-center gap-2">
            <span className="material-symbols-outlined text-[18px]">edit_note</span>
            Flag
          </button>
        </div>
      </div>
    </aside>
  )
}

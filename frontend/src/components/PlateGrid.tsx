import { useMemo } from 'react'
import type { Well, Plate, FeatureType } from '../types/projects'
import { getWellColor, FEATURE_FILTERS } from '../mocks/experimentDetail'

interface PlateGridProps {
  plate: Plate
  wells: Well[]
  selectedWell: Well | null
  onWellSelect: (well: Well) => void
  selectedFeature: FeatureType
  onFeatureChange: (feature: FeatureType) => void
}

export function PlateGrid({
  plate,
  wells,
  selectedWell,
  onWellSelect,
  selectedFeature,
  onFeatureChange,
}: PlateGridProps) {
  // Create a map for quick well lookup
  const wellMap = useMemo(() => {
    const map = new Map<string, Well>()
    wells.forEach((well) => {
      const key = `${well.row}-${well.column}`
      map.set(key, well)
    })
    return map
  }, [wells])

  // Generate row labels (A-P for 384-well)
  const rowLabels = useMemo(() => {
    return Array.from({ length: plate.rows }, (_, i) => String.fromCharCode(65 + i))
  }, [plate.rows])

  // Generate column labels (01-24 for 384-well)
  const colLabels = useMemo(() => {
    return Array.from({ length: plate.columns }, (_, i) => String(i + 1).padStart(2, '0'))
  }, [plate.columns])

  // Get current feature filter
  const currentFilter = FEATURE_FILTERS.find((f) => f.type === selectedFeature) || FEATURE_FILTERS[0]

  return (
    <div className="flex flex-col h-full">
      {/* Filters / Toolbar */}
      <div className="flex-none px-8 py-4 flex items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-[#111a22]/50 backdrop-blur-sm z-10">
        <div className="flex items-center gap-3 overflow-x-auto">
          <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mr-2">Color by:</p>
          {FEATURE_FILTERS.map((filter) => (
            <button
              key={filter.type}
              onClick={() => onFeatureChange(filter.type)}
              className={`flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-full px-4 transition-all active:scale-95 ${
                selectedFeature === filter.type
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                  : 'bg-white border border-slate-200 dark:bg-slate-800 dark:border-slate-700 hover:border-slate-400'
              }`}
            >
              <span
                className={`size-2 rounded-full ${
                  filter.colorScale === 'green'
                    ? 'bg-emerald-500'
                    : filter.colorScale === 'blue'
                      ? 'bg-blue-500'
                      : filter.colorScale === 'purple'
                        ? 'bg-purple-500'
                        : 'bg-amber-500'
                }`}
              />
              <span className="text-xs font-bold uppercase tracking-wide">{filter.label}</span>
            </button>
          ))}
        </div>
        <div className="flex items-center gap-3 text-sm text-slate-500 dark:text-slate-400">
          <span className="flex items-center gap-1">
            <span className="material-symbols-outlined text-[18px]">zoom_in</span> Zoom
          </span>
          <div className="h-4 w-[1px] bg-slate-300 dark:bg-slate-700 mx-1"></div>
          <span className="flex items-center gap-1 cursor-pointer hover:text-primary transition-colors">
            <span className="material-symbols-outlined text-[18px]">download</span> Export Map
          </span>
        </div>
      </div>

      {/* Plate Grid Container */}
      <div className="flex-1 overflow-auto p-8 flex items-start justify-center bg-slate-50/50 dark:bg-[#0c1218]">
        <div className="bg-white dark:bg-[#16202a] rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-6 w-full max-w-6xl mx-auto overflow-x-auto">
          {/* Grid Wrapper */}
          <div className="min-w-[900px]">
            {/* Top Labels (01-24) */}
            <div className="flex mb-2">
              <div className="w-8 flex-none"></div>
              <div className="flex flex-1 gap-0.5">
                {colLabels.map((label) => (
                  <div
                    key={label}
                    className="w-6 text-center text-[10px] font-bold text-slate-400"
                  >
                    {label}
                  </div>
                ))}
              </div>
            </div>

            {/* Rows */}
            <div className="flex flex-col gap-0.5">
              {rowLabels.map((rowLabel, rowIndex) => (
                <div key={rowLabel} className="flex items-center">
                  <div className="w-8 flex-none text-center text-xs font-bold text-slate-400">
                    {rowLabel}
                  </div>
                  <div className="flex flex-1 gap-0.5">
                    {colLabels.map((_, colIndex) => {
                      const well = wellMap.get(`${rowIndex}-${colIndex}`)
                      if (!well) return null

                      const colors = getWellColor(well, selectedFeature)
                      const isSelected = selectedWell?.id === well.id

                      return (
                        <div
                          key={`${rowIndex}-${colIndex}`}
                          className="relative w-6 h-6 flex items-center justify-center"
                        >
                          {isSelected && (
                            <div className="absolute inset-0 rounded-full ring-2 ring-primary ring-offset-1 ring-offset-white dark:ring-offset-[#16202a] z-10"></div>
                          )}
                          <button
                            onClick={() => !well.is_empty && onWellSelect(well)}
                            disabled={well.is_empty}
                            className={`w-full h-full rounded-full border flex items-center justify-center transition-transform ${
                              well.is_empty
                                ? 'cursor-default opacity-50'
                                : 'cursor-pointer hover:scale-110'
                            } ${colors.bg} ${colors.border}`}
                          >
                            {!well.is_empty && colors.indicator && (
                              <span className={`size-1 rounded-full ${colors.indicator}`}></span>
                            )}
                          </button>
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Legend / Footer */}
      <div className="flex-none bg-white border-t border-slate-200 dark:bg-[#16202a] dark:border-slate-800 px-8 py-3 flex gap-6 text-xs text-slate-500 font-medium">
        <div className="flex items-center gap-2">
          <div
            className={`size-3 rounded-full ${
              currentFilter.colorScale === 'green'
                ? 'bg-emerald-100 border border-emerald-200'
                : currentFilter.colorScale === 'blue'
                  ? 'bg-blue-100 border border-blue-200'
                  : currentFilter.colorScale === 'purple'
                    ? 'bg-purple-100 border border-purple-200'
                    : 'bg-amber-100 border border-amber-200'
            } flex items-center justify-center`}
          >
            <span
              className={`size-1 rounded-full ${
                currentFilter.colorScale === 'green'
                  ? 'bg-emerald-500'
                  : currentFilter.colorScale === 'blue'
                    ? 'bg-blue-500'
                    : currentFilter.colorScale === 'purple'
                      ? 'bg-purple-500'
                      : 'bg-amber-500'
              }`}
            ></span>
          </div>
          <span>High {currentFilter.label}</span>
        </div>
        <div className="flex items-center gap-2">
          <div
            className={`size-3 rounded-full ${
              currentFilter.colorScale === 'green'
                ? 'bg-emerald-50 border border-emerald-100'
                : currentFilter.colorScale === 'blue'
                  ? 'bg-blue-50 border border-blue-100'
                  : currentFilter.colorScale === 'purple'
                    ? 'bg-purple-50 border border-purple-100'
                    : 'bg-amber-50 border border-amber-100'
            } flex items-center justify-center`}
          >
            <span
              className={`size-1 rounded-full ${
                currentFilter.colorScale === 'green'
                  ? 'bg-emerald-400'
                  : currentFilter.colorScale === 'blue'
                    ? 'bg-blue-400'
                    : currentFilter.colorScale === 'purple'
                      ? 'bg-purple-400'
                      : 'bg-amber-400'
              }`}
            ></span>
          </div>
          <span>Low {currentFilter.label}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="size-3 rounded-full bg-slate-100 border border-slate-200"></div>
          <span>Empty / Unscanned</span>
        </div>
      </div>
    </div>
  )
}

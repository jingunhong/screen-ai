import { useState, useMemo, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import type { Experiment, Well, FeatureType } from '../types/projects'
import { PlateGrid } from '../components/PlateGrid'
import { WellDetailPanel } from '../components/WellDetailPanel'
import { generateMockPlates, generateMockWells, generateMockImages } from '../mocks/experimentDetail'
import experimentsData from '../mocks/experiments.json'
import { useAuth } from '../hooks/useAuth'

export default function ExperimentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  // Find the experiment from mock data
  const experiment = useMemo(() => {
    const expId = parseInt(id || '1', 10)
    return (experimentsData as Experiment[]).find((exp) => exp.id === expId) || null
  }, [id])

  // Generate mock plates for this experiment
  const plates = useMemo(() => {
    if (!experiment) return []
    return generateMockPlates(experiment.id)
  }, [experiment])

  // State for selected plate (always non-null, defaults to first plate)
  const [selectedPlateId, setSelectedPlateId] = useState<string | null>(null)

  // Set default plate when plates change
  useEffect(() => {
    if (plates.length > 0 && !selectedPlateId) {
      setSelectedPlateId(plates[0].id)
    }
  }, [plates, selectedPlateId])

  // Get the selected plate
  const selectedPlate = useMemo(() => {
    return plates.find((p) => p.id === selectedPlateId) || plates[0] || null
  }, [plates, selectedPlateId])

  // Generate wells for selected plate
  const wells = useMemo(() => {
    if (!selectedPlate) return []
    return generateMockWells(selectedPlate)
  }, [selectedPlate])

  // State for selected well (always non-null, defaults to first non-empty well)
  const [selectedWellId, setSelectedWellId] = useState<string | null>(null)

  // Set default well when wells change
  useEffect(() => {
    if (wells.length > 0) {
      const firstNonEmpty = wells.find((w) => !w.is_empty)
      if (firstNonEmpty && !selectedWellId) {
        setSelectedWellId(firstNonEmpty.id)
      } else if (firstNonEmpty && !wells.find((w) => w.id === selectedWellId)) {
        // Reset to first non-empty if current selection is no longer valid
        setSelectedWellId(firstNonEmpty.id)
      }
    }
  }, [wells, selectedWellId])

  // Get the selected well
  const selectedWell = useMemo(() => {
    return wells.find((w) => w.id === selectedWellId) || wells.find((w) => !w.is_empty) || null
  }, [wells, selectedWellId])

  // Generate images for selected well
  const wellImages = useMemo(() => {
    if (!selectedWell) return []
    return generateMockImages(selectedWell)
  }, [selectedWell])

  // Feature filter state
  const [selectedFeature, setSelectedFeature] = useState<FeatureType>('cell_count')

  const handleWellSelect = (well: Well) => {
    setSelectedWellId(well.id)
  }

  const handlePlateSelect = (plateId: string) => {
    setSelectedPlateId(plateId)
    setSelectedWellId(null) // Reset well selection when changing plates
  }

  const handleBackClick = () => {
    navigate('/')
  }

  if (!experiment) {
    return (
      <div className="h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Experiment not found</h2>
          <button onClick={handleBackClick} className="text-primary hover:underline">
            Back to experiments
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-slate-50 dark:bg-background-dark h-screen flex flex-col">
      {/* Top Navigation */}
      <header className="flex-none flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 bg-white dark:bg-[#111a22] px-6 py-3 shadow-sm z-20">
        <div className="flex items-center gap-4">
          <div className="size-8 rounded bg-primary/10 text-primary flex items-center justify-center">
            <span className="material-symbols-outlined">grid_on</span>
          </div>
          <h2 className="text-slate-900 dark:text-white text-lg font-bold leading-tight tracking-tight">
            Plate Layout Explorer
          </h2>
        </div>
        <div className="flex flex-1 justify-end gap-6 items-center">
          <div className="hidden md:flex flex-col min-w-40 h-10 w-96">
            <div className="flex w-full flex-1 items-stretch rounded-lg h-full relative">
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500 flex items-center justify-center pointer-events-none">
                <span className="material-symbols-outlined text-[20px]">search</span>
              </div>
              <input
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:border-primary h-full placeholder:text-slate-400 px-4 pl-10 text-sm font-normal leading-normal transition-all"
                placeholder="Search experiments, plates or IDs..."
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button className="flex items-center justify-center rounded-lg h-10 px-4 bg-primary hover:bg-blue-600 transition-colors text-white text-sm font-bold leading-normal tracking-wide shadow-md shadow-primary/20">
              <span className="truncate">New Experiment</span>
            </button>
            <button className="flex items-center justify-center rounded-lg size-10 bg-white border border-slate-200 dark:bg-slate-800 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
              <span className="material-symbols-outlined">settings</span>
            </button>
            <button className="flex items-center justify-center rounded-full size-10 overflow-hidden border border-slate-200 dark:border-slate-700 ml-2 bg-blue-600 text-white font-semibold text-sm">
              {user?.full_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Left Sidebar */}
        <aside className="flex w-72 flex-col border-r border-slate-200 bg-white h-full shrink-0">
          {/* Sidebar Header with Back Button */}
          <div className="p-6 pb-4">
            <button
              onClick={handleBackClick}
              className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-900 transition-colors mb-4"
            >
              <span className="material-symbols-outlined text-[18px]">arrow_back</span>
              <span>Back to Experiments</span>
            </button>

            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5"
                  />
                </svg>
              </div>
              <div className="flex-1 min-w-0">
                <h1 className="text-lg font-bold tracking-tight text-slate-900 truncate">
                  {experiment.name}
                </h1>
                <p className="text-xs text-slate-500 truncate">{experiment.project_name}</p>
              </div>
            </div>

            {experiment.description && (
              <p className="text-xs text-slate-500 mb-4 line-clamp-2">{experiment.description}</p>
            )}
          </div>

          {/* Plates List */}
          <div className="flex-1 overflow-y-auto px-3 py-2">
            <div className="px-3 mb-2">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Plates ({plates.length})
              </h3>
            </div>
            <div className="flex flex-col gap-1">
              {plates.map((plate) => {
                const isSelected = selectedPlateId === plate.id
                return (
                  <button
                    key={plate.id}
                    onClick={() => handlePlateSelect(plate.id)}
                    className={`flex items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors ${
                      isSelected
                        ? 'bg-blue-50 text-blue-600 font-medium'
                        : 'text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    <span className="material-symbols-outlined text-[18px]">grid_view</span>
                    <span className="truncate">{plate.name}</span>
                    <span
                      className={`ml-auto text-xs ${isSelected ? 'text-blue-500' : 'text-slate-400'}`}
                    >
                      {plate.format}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* User Profile Footer */}
          <div className="border-t border-slate-200 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-white font-semibold text-sm">
                {user?.full_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 truncate">
                  {user?.full_name || 'User'}
                </p>
                <p className="text-xs text-slate-500 truncate">{user?.email}</p>
              </div>
              <button
                onClick={() => logout()}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
                title="Logout"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"
                  />
                </svg>
              </button>
            </div>
          </div>
        </aside>

        {/* Main Content: Plate Grid */}
        <main className="flex-1 flex flex-col overflow-hidden min-w-0">
          {selectedPlate && (
            <PlateGrid
              plate={selectedPlate}
              wells={wells}
              selectedWell={selectedWell}
              onWellSelect={handleWellSelect}
              selectedFeature={selectedFeature}
              onFeatureChange={setSelectedFeature}
            />
          )}
        </main>

        {/* Right Panel: Well Details */}
        {selectedWell && selectedPlate && (
          <WellDetailPanel well={selectedWell} plate={selectedPlate} images={wellImages} />
        )}
      </div>
    </div>
  )
}

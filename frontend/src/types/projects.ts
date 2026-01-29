export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Experiment {
  id: number
  name: string
  description?: string
  project_id: number
  project_name: string
  plate_count: number
  status: 'ready' | 'processing' | 'failed'
  created_at: string
  updated_at: string
}

export interface ProjectWithExperiments extends Project {
  experiments: Experiment[]
}

export interface Plate {
  id: string
  name: string
  experiment_id: number
  format: 96 | 384 | 1536
  rows: number
  columns: number
  created_at: string
  updated_at: string
}

export interface Well {
  id: string
  plate_id: string
  row: number
  column: number
  position: string // e.g., "A01", "B12"
  is_empty: boolean
  compound_id?: string
  compound_name?: string
  concentration?: number
  concentration_unit?: string
  cell_line?: string
  incubation_hours?: number
  cell_count?: number
  viability?: number
  qc_score?: number
  analyst_notes?: string
  analyst_name?: string
  notes_updated_at?: string
}

export interface WellImage {
  id: string
  well_id: string
  channel: string // e.g., "DAPI", "GFP", "RFP"
  thumbnail_url: string
  full_url?: string
}

export type FeatureType = 'cell_count' | 'viability' | 'concentration' | 'qc_score'

export interface FeatureFilter {
  type: FeatureType
  label: string
  colorScale: 'green' | 'blue' | 'purple' | 'orange'
}

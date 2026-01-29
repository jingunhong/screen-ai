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

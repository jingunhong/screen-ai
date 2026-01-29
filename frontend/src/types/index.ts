// User types
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Auth types
export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  username: string; // email
  password: string;
}

// Project types
export interface Project {
  id: string;
  name: string;
  description: string | null;
  owner_id: string;
  experiment_count: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
}

// Experiment types
export interface Experiment {
  id: string;
  name: string;
  description: string | null;
  project_id: string;
  plate_count: number;
  created_at: string;
  updated_at: string;
}

export interface ExperimentCreate {
  name: string;
  description?: string;
}

// Plate types
export interface Plate {
  id: string;
  name: string;
  barcode: string | null;
  description: string | null;
  experiment_id: string;
  rows: number;
  columns: number;
  well_count: number;
  format_name: string;
  created_at: string;
  updated_at: string;
}

export interface PlateCreate {
  name: string;
  barcode?: string;
  description?: string;
  rows?: number;
  columns?: number;
}

// Well types
export interface Well {
  id: string;
  plate_id: string;
  row: number;
  column: number;
  compound_id: string | null;
  concentration: number | null;
  concentration_unit: string;
  well_type: string;
  row_label: string;
  column_label: string;
  position: string;
  created_at: string;
  updated_at: string;
}

export interface WellGridItem {
  id: string;
  row: number;
  column: number;
  position: string;
  well_type: string;
  compound_id: string | null;
  concentration: number | null;
  cell_count: number | null;
  viability: number | null;
  z_score: number | null;
}

// Pagination types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

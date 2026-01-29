import type { Plate, Well, WellImage, FeatureFilter, FeatureType } from '../types/projects'

// Image URLs from the mockup
const MOCK_IMAGE_URLS = [
  'https://lh3.googleusercontent.com/aida-public/AB6AXuAhtrTE3v8AVWdyQ1Cs8_bdfdKAAaP1f6N8CiwhDPk3swfK7WVQh3Kz_v6hOiZZ5KYFpdke6Pfy2gyNMOMGrq90rzCP8ctyquFYnOU7viIQfPVvL2YzLQnGwzvcO5EpVZA_G7eKoxowrEn0Kl2xL0yR9e-njjsuXj0mdzx2Z_w9dTHVGM0BQs2SUJY3I_BSPO4xeY0Zn_6SY3IIE5Y0F6GN6biLeogBpQ22Pn4f3ji8_Vv0Y_dSPjuX-Q8JWrpAsX3F3awXQ4bKTM4',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCTRijvTNkF038586EKKEm5clqhYrK87OPEveH8i5Aqxb5rXOVX-W5pXf9IHb-LEhTzoVTCebAxT5I9APFy5U0iGHAu2PrJZ_jfVX49EAjMrdZ2JNxeh_Ep2ylC1ytHMC8aQVqWMHUjb7OvqK_UHIMbS5GEOzkO8mH2VH-qgDm4WUwZX-ZM6tjnDGMKAAj0EkzfrBer5CGAY04qqTA-VwraU3FHcfUDE0tAC8TL2DJkjSVcpDk9aWGwQJPej9gHkcw8oordZeDVE2o',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuAIOvkWZpH9W7ZtgfbSdC9DJZIP07qYO9GVh3KMmfBpWib9Zxzx1SddWkgh-vB0XCDmOQbS0R75NEpKubbi1GPbORDCXL_7KF63XSOqlBCOXYDT5_KpD6_D4ZzW8hU4osFGbaBoG-BWQHP_EjKVujWN08jkP9RgvvvS459QO3kz-9_HdLt-o1dvVvWdqE6D_AqeGCLTq2IcNlizB2mQUzrgENLI1gviysorp3R-eYyUrtu6pwBw0pyL8L5u5r1EHUklEKIqQz9IKZc',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuBfVrcChBvLrxyopGKys5OBOc1O8cgHHq1NeKozNkIlZb7cE2HrOV84LdiHlUfv5auu7FoQAxDSeDMzWC0GNPQ35BmC9ZYiBHmVQau7VvT6LfWOuSa48gAUDacqoYf_x103qgy1iJd4j-zvoUcoNjetP9NhnNDANeT_PNWNWgDSPbkQd0oLUVvvFtFtVDoKUqP8wqHZHLZ0PTFT8Pj0_RBH7Bbk-J0roO2Rkvw8iNegIkfnLsNCGMVyNhJP3LgYjfNk665J1efLuUs',
]

// Helper to generate position string (e.g., "A01", "P24")
function getPositionString(row: number, col: number): string {
  const rowLetter = String.fromCharCode(65 + row) // A=0, B=1, etc.
  const colNumber = String(col + 1).padStart(2, '0')
  return `${rowLetter}${colNumber}`
}

// Compounds for mock data
const COMPOUNDS = [
  { id: 'cpd-001', name: 'Staurosporine' },
  { id: 'cpd-002', name: 'Doxorubicin' },
  { id: 'cpd-003', name: 'Paclitaxel' },
  { id: 'cpd-004', name: 'Vincristine' },
  { id: 'cpd-005', name: 'Cisplatin' },
  { id: 'cpd-006', name: 'Etoposide' },
  { id: 'cpd-007', name: 'Methotrexate' },
  { id: 'cpd-008', name: 'Imatinib' },
]

const CELL_LINES = ['HEK293', 'HeLa', 'MCF7', 'A549', 'U2OS']
const CONCENTRATIONS = [0.01, 0.1, 1, 10, 100] // in µM

// Analyst notes for some wells
const ANALYST_NOTES = [
  {
    note: 'Shows slightly irregular staining in the second channel. Flagged for manual review. Focus looks consistent.',
    name: 'Dr. Smith',
    time: '2h ago',
  },
  {
    note: 'Strong signal in DAPI channel. Cell morphology appears normal.',
    name: 'Dr. Johnson',
    time: '4h ago',
  },
  {
    note: 'Possible contamination detected. Recommend re-imaging.',
    name: 'Dr. Lee',
    time: '1d ago',
  },
  {
    note: 'Excellent cell confluency. Ideal for analysis.',
    name: 'Dr. Chen',
    time: '3h ago',
  },
]

// Generate mock plates for an experiment
export function generateMockPlates(experimentId: number): Plate[] {
  return [
    {
      id: `plate-${experimentId}-001`,
      name: 'Plate 001',
      experiment_id: experimentId,
      format: 384,
      rows: 16,
      columns: 24,
      created_at: '2023-10-20T10:00:00Z',
      updated_at: '2023-10-24T14:30:00Z',
    },
    {
      id: `plate-${experimentId}-002`,
      name: 'Plate 002',
      experiment_id: experimentId,
      format: 384,
      rows: 16,
      columns: 24,
      created_at: '2023-10-21T09:00:00Z',
      updated_at: '2023-10-24T15:00:00Z',
    },
    {
      id: `plate-${experimentId}-003`,
      name: 'Plate 003',
      experiment_id: experimentId,
      format: 384,
      rows: 16,
      columns: 24,
      created_at: '2023-10-22T11:00:00Z',
      updated_at: '2023-10-24T16:00:00Z',
    },
  ]
}

// Generate mock wells for a 384-well plate
export function generateMockWells(plate: Plate): Well[] {
  const wells: Well[] = []
  const seed = parseInt(plate.id.split('-').pop() || '1', 10)

  for (let row = 0; row < plate.rows; row++) {
    for (let col = 0; col < plate.columns; col++) {
      const position = getPositionString(row, col)
      const wellIndex = row * plate.columns + col

      // Determine if well is empty (edges and some random wells)
      const isEdge = row === 0 || row === plate.rows - 1 || col === 0 || col === plate.columns - 1
      const randomEmpty = Math.sin(wellIndex * seed) > 0.85
      const isEmpty = isEdge || randomEmpty

      if (isEmpty) {
        wells.push({
          id: `well-${plate.id}-${position}`,
          plate_id: plate.id,
          row,
          column: col,
          position,
          is_empty: true,
        })
      } else {
        // Generate random but deterministic values
        const compoundIndex = Math.abs(Math.floor(Math.sin(wellIndex * seed * 2) * COMPOUNDS.length))
        const compound = COMPOUNDS[compoundIndex % COMPOUNDS.length]
        const cellLineIndex = Math.abs(Math.floor(Math.sin(wellIndex * seed * 3) * CELL_LINES.length))
        const cellLine = CELL_LINES[cellLineIndex % CELL_LINES.length]
        const concIndex = Math.abs(Math.floor(Math.sin(wellIndex * seed * 4) * CONCENTRATIONS.length))
        const concentration = CONCENTRATIONS[concIndex % CONCENTRATIONS.length]

        // Cell count: 500-5000, biased by position
        const baseCellCount = 2500
        const cellCountVariation = Math.sin(wellIndex * seed * 5) * 2000
        const cellCount = Math.round(baseCellCount + cellCountVariation)

        // Viability: 0.3-1.0
        const baseViability = 0.7
        const viabilityVariation = Math.sin(wellIndex * seed * 6) * 0.3
        const viability = Math.max(0.3, Math.min(1.0, baseViability + viabilityVariation))

        // QC Score: 0.5-1.0
        const baseQcScore = 0.8
        const qcVariation = Math.sin(wellIndex * seed * 7) * 0.25
        const qcScore = Math.max(0.5, Math.min(1.0, baseQcScore + qcVariation))

        // Add analyst notes to some wells
        const hasNotes = Math.sin(wellIndex * seed * 8) > 0.7
        const noteIndex = Math.abs(Math.floor(Math.sin(wellIndex * seed * 9) * ANALYST_NOTES.length))
        const analystNote = hasNotes ? ANALYST_NOTES[noteIndex % ANALYST_NOTES.length] : null

        wells.push({
          id: `well-${plate.id}-${position}`,
          plate_id: plate.id,
          row,
          column: col,
          position,
          is_empty: false,
          compound_id: compound.id,
          compound_name: compound.name,
          concentration,
          concentration_unit: 'µM',
          cell_line: cellLine,
          incubation_hours: 24,
          cell_count: Math.max(100, cellCount),
          viability: Math.round(viability * 100) / 100,
          qc_score: Math.round(qcScore * 100) / 100,
          analyst_notes: analystNote?.note,
          analyst_name: analystNote?.name,
          notes_updated_at: analystNote?.time,
        })
      }
    }
  }

  return wells
}

// Generate mock images for a well
export function generateMockImages(well: Well): WellImage[] {
  if (well.is_empty) return []

  // Use deterministic selection based on well position
  const wellIndex = well.row * 24 + well.column
  const channels = ['DAPI', 'GFP', 'RFP', 'Merged']

  return channels.map((channel, i) => ({
    id: `img-${well.id}-${channel}`,
    well_id: well.id,
    channel,
    thumbnail_url: MOCK_IMAGE_URLS[(wellIndex + i) % MOCK_IMAGE_URLS.length],
    full_url: MOCK_IMAGE_URLS[(wellIndex + i) % MOCK_IMAGE_URLS.length],
  }))
}

// Feature filter options
export const FEATURE_FILTERS: FeatureFilter[] = [
  { type: 'cell_count', label: 'Cell Count', colorScale: 'blue' },
  { type: 'viability', label: 'Viability', colorScale: 'green' },
  { type: 'concentration', label: 'Concentration', colorScale: 'purple' },
  { type: 'qc_score', label: 'QC Score', colorScale: 'orange' },
]

// Get color class based on feature value and type
export function getWellColor(
  well: Well,
  featureType: FeatureType
): { bg: string; border: string; indicator: string } {
  if (well.is_empty) {
    return {
      bg: 'bg-slate-100 dark:bg-slate-800',
      border: 'border-slate-200 dark:border-slate-700',
      indicator: '',
    }
  }

  let normalizedValue = 0
  switch (featureType) {
    case 'cell_count':
      // Normalize cell count: 100-5000 -> 0-1
      normalizedValue = Math.min(1, Math.max(0, ((well.cell_count || 0) - 100) / 4900))
      break
    case 'viability':
      normalizedValue = well.viability || 0
      break
    case 'concentration':
      // Log scale for concentration: 0.01-100 -> 0-1
      normalizedValue = Math.log10((well.concentration || 0.01) / 0.01) / 4
      break
    case 'qc_score':
      normalizedValue = well.qc_score || 0
      break
  }

  // Color intensity based on normalized value (0-1)
  const intensity = Math.round(normalizedValue * 100)

  // Color scheme based on feature type
  const colorSchemes = {
    cell_count: {
      bg: intensity > 70 ? 'bg-blue-200' : intensity > 40 ? 'bg-blue-100' : 'bg-blue-50',
      border: 'border-blue-200 dark:border-blue-800',
      indicator: intensity > 70 ? 'bg-blue-600' : intensity > 40 ? 'bg-blue-500' : 'bg-blue-400',
    },
    viability: {
      bg: intensity > 70 ? 'bg-emerald-200' : intensity > 40 ? 'bg-emerald-100' : 'bg-rose-100',
      border:
        intensity > 40
          ? 'border-emerald-200 dark:border-emerald-800'
          : 'border-rose-200 dark:border-rose-800',
      indicator: intensity > 70 ? 'bg-emerald-600' : intensity > 40 ? 'bg-emerald-500' : 'bg-rose-500',
    },
    concentration: {
      bg: intensity > 70 ? 'bg-purple-200' : intensity > 40 ? 'bg-purple-100' : 'bg-purple-50',
      border: 'border-purple-200 dark:border-purple-800',
      indicator: intensity > 70 ? 'bg-purple-600' : intensity > 40 ? 'bg-purple-500' : 'bg-purple-400',
    },
    qc_score: {
      bg: intensity > 70 ? 'bg-amber-100' : intensity > 40 ? 'bg-amber-50' : 'bg-rose-100',
      border:
        intensity > 40
          ? 'border-amber-200 dark:border-amber-800'
          : 'border-rose-200 dark:border-rose-800',
      indicator: intensity > 70 ? 'bg-emerald-500' : intensity > 40 ? 'bg-amber-500' : 'bg-rose-500',
    },
  }

  return colorSchemes[featureType]
}

import { Link } from 'react-router-dom'
import type { Experiment } from '../types/projects'

interface ExperimentsTableProps {
  experiments: Experiment[]
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function StatusBadge({ status }: { status: Experiment['status'] }) {
  const styles = {
    ready: 'bg-emerald-100 text-emerald-700',
    processing: 'bg-blue-100 text-blue-700',
    failed: 'bg-red-100 text-red-700',
  }

  const labels = {
    ready: 'Ready',
    processing: 'Processing',
    failed: 'QC Failed',
  }

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${styles[status]}`}
    >
      {status === 'ready' && <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />}
      {status === 'processing' && (
        <svg className="h-3 w-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
      )}
      {status === 'failed' && (
        <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
      )}
      {labels[status]}
    </span>
  )
}

export default function ExperimentsTable({ experiments }: ExperimentsTableProps) {
  if (experiments.length === 0) {
    return (
      <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
        <svg
          className="mx-auto h-12 w-12 text-slate-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1}
            d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5"
          />
        </svg>
        <h3 className="mt-4 text-lg font-semibold text-slate-900">No experiments found</h3>
        <p className="mt-2 text-slate-500">
          Select a project or create a new experiment to get started.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
      <table className="min-w-full text-left">
        <thead className="border-b border-slate-200 bg-slate-50">
          <tr>
            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Experiment Name
            </th>
            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
              ID
            </th>
            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Plate Count
            </th>
            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Last Modified
            </th>
            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Status
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {experiments.map((experiment) => (
            <tr key={experiment.id} className="hover:bg-slate-50 transition-colors">
              <td className="px-6 py-4">
                <div className="flex flex-col">
                  <Link
                    to={`/experiments/${experiment.id}`}
                    className="font-semibold text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    {experiment.name}
                  </Link>
                  <span className="text-xs text-slate-500">{experiment.project_name}</span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-slate-600">
                Exp-{experiment.id.toString().padStart(4, '0')}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                <div className="flex items-center gap-1.5">
                  <svg
                    className="h-4 w-4 text-slate-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"
                    />
                  </svg>
                  {experiment.plate_count} Plates
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                {formatDate(experiment.updated_at)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <StatusBadge status={experiment.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

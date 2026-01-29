import { useState } from 'react'
import type { Project, Experiment } from '../types/projects'

interface ProjectTreeProps {
  projects: Project[]
  experiments: Experiment[]
  selectedProjectId: number | null
  selectedExperimentId: number | null
  onProjectSelect: (projectId: number | null) => void
  onExperimentSelect: (experimentId: number) => void
}

export default function ProjectTree({
  projects,
  experiments,
  selectedProjectId,
  selectedExperimentId,
  onProjectSelect,
  onExperimentSelect,
}: ProjectTreeProps) {
  const [expandedProjects, setExpandedProjects] = useState<Set<number>>(new Set([1]))

  const toggleProject = (projectId: number) => {
    setExpandedProjects((prev) => {
      const next = new Set(prev)
      if (next.has(projectId)) {
        next.delete(projectId)
      } else {
        next.add(projectId)
      }
      return next
    })
  }

  const handleProjectClick = (projectId: number) => {
    toggleProject(projectId)
    onProjectSelect(selectedProjectId === projectId ? null : projectId)
  }

  const getExperimentsForProject = (projectId: number) => {
    return experiments.filter((exp) => exp.project_id === projectId)
  }

  return (
    <aside className="flex w-72 flex-col border-r border-slate-200 bg-white h-full shrink-0">
      {/* Sidebar Header */}
      <div className="p-6 pb-4">
        <div className="flex items-center gap-3 mb-6">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
              />
            </svg>
          </div>
          <h1 className="text-lg font-bold tracking-tight text-slate-900">Screen AI</h1>
        </div>
        <button className="flex w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors h-10 px-4 text-white text-sm font-semibold shadow-sm">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span>New Experiment</span>
        </button>
      </div>

      {/* Tree Content */}
      <div className="flex-1 overflow-y-auto px-3 py-2">
        <div className="flex flex-col gap-1">
          {projects.map((project) => {
            const isExpanded = expandedProjects.has(project.id)
            const isSelected = selectedProjectId === project.id
            const projectExperiments = getExperimentsForProject(project.id)

            return (
              <div key={project.id}>
                <button
                  onClick={() => handleProjectClick(project.id)}
                  className={`flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm font-medium transition-colors ${
                    isSelected ? 'bg-slate-100 text-slate-900' : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <svg
                    className={`h-5 w-5 ${isSelected ? 'text-slate-600' : 'text-slate-400'}`}
                    fill={isExpanded ? 'currentColor' : 'none'}
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z"
                    />
                  </svg>
                  <span className="flex-1 truncate">{project.name}</span>
                  <svg
                    className={`h-4 w-4 text-slate-400 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>

                {/* Experiments under project */}
                {isExpanded && projectExperiments.length > 0 && (
                  <div className="ml-3 mt-1 flex flex-col gap-1 border-l border-slate-200 pl-3">
                    {projectExperiments.map((experiment) => {
                      const isExpSelected = selectedExperimentId === experiment.id
                      return (
                        <button
                          key={experiment.id}
                          onClick={() => onExperimentSelect(experiment.id)}
                          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors ${
                            isExpSelected
                              ? 'bg-blue-50 text-blue-600 font-medium'
                              : 'text-slate-600 hover:bg-slate-50'
                          }`}
                        >
                          <svg
                            className="h-4 w-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={1.5}
                              d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5"
                            />
                          </svg>
                          <span className="truncate">{experiment.name}</span>
                        </button>
                      )
                    })}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </aside>
  )
}

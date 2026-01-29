import { useState, useMemo } from 'react'
import { useAuth } from '../hooks/useAuth'
import ProjectTree from '../components/ProjectTree'
import ExperimentsTable from '../components/ExperimentsTable'
import type { Project, Experiment } from '../types/projects'

import projectsData from '../mocks/projects.json'
import experimentsData from '../mocks/experiments.json'

export default function ProjectsExperimentsPage() {
  const { user, logout } = useAuth()
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null)
  const [selectedExperimentId, setSelectedExperimentId] = useState<number | null>(null)

  const projects: Project[] = projectsData
  const experiments: Experiment[] = experimentsData as Experiment[]

  const filteredExperiments = useMemo(() => {
    if (selectedProjectId === null) {
      return experiments
    }
    return experiments.filter((exp) => exp.project_id === selectedProjectId)
  }, [experiments, selectedProjectId])

  const handleProjectSelect = (projectId: number | null) => {
    setSelectedProjectId(projectId)
    setSelectedExperimentId(null)
  }

  const handleExperimentSelect = (experimentId: number) => {
    setSelectedExperimentId(experimentId)
  }

  const selectedProject = projects.find((p) => p.id === selectedProjectId)

  return (
    <div className="flex h-screen w-full bg-slate-50">
      {/* Sidebar */}
      <div className="flex flex-col h-full">
        <ProjectTree
          projects={projects}
          experiments={experiments}
          selectedProjectId={selectedProjectId}
          selectedExperimentId={selectedExperimentId}
          onProjectSelect={handleProjectSelect}
          onExperimentSelect={handleExperimentSelect}
        />
        {/* User Profile Footer */}
        <div className="w-72 border-r border-t border-slate-200 bg-white p-4">
          <div className="flex w-full items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-600">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                  />
                </svg>
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-medium text-slate-900">
                  {user?.full_name || user?.email || 'User'}
                </span>
                <span className="text-xs text-slate-500">{user?.email}</span>
              </div>
            </div>
            <button
              onClick={logout}
              className="rounded p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors"
              title="Sign Out"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      </div>

      {/* Main Content */}
      <main className="flex h-full flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="px-8 pt-8 pb-6 shrink-0">
          {/* Breadcrumbs */}
          <nav className="flex items-center text-sm font-medium text-slate-500 mb-4">
            <span className="hover:text-blue-600 cursor-pointer transition-colors">Home</span>
            {selectedProject && (
              <>
                <span className="mx-2 text-slate-400">/</span>
                <span className="text-slate-900">{selectedProject.name}</span>
              </>
            )}
          </nav>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">
            {selectedProject ? `${selectedProject.name} - Experiments` : 'All Experiments'}
          </h2>
          {selectedProject?.description && (
            <p className="mt-1 text-slate-500">{selectedProject.description}</p>
          )}
        </header>

        {/* Table Container */}
        <div className="flex-1 overflow-auto px-8 pb-8">
          <ExperimentsTable experiments={filteredExperiments} />
        </div>
      </main>
    </div>
  )
}

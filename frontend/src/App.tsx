import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">
        Screen AI
      </h1>
      <p className="text-gray-600 mb-6">
        Drug Discovery Screening Data Management Platform
      </p>
      <div className="bg-white rounded-lg shadow-md p-6">
        <button
          onClick={() => setCount((count) => count + 1)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors"
        >
          Count is {count}
        </button>
        <p className="text-sm text-gray-500 mt-4">
          Edit <code className="bg-gray-100 px-1 rounded">src/App.tsx</code> and save to test HMR
        </p>
      </div>
    </div>
  )
}

export default App

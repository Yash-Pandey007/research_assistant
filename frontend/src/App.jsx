import React, { useState } from 'react';
import ResultDisplay from './components/ResultDisplay';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Research Assistant
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Ask anything. I'll search the web and synthesize an answer for you.
          </p>
        </div>

        <form onSubmit={handleSearch} className="mt-8 sm:flex justify-center">
          <div className="min-w-0 flex-1">
            <label htmlFor="query" className="sr-only">
              Ask a question
            </label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="block w-full px-4 py-3 rounded-md border border-gray-300 text-base text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="What do you want to know?"
            />
          </div>
          <div className="mt-3 sm:mt-0 sm:ml-3">
            <button
              type="submit"
              disabled={loading}
              className={`block w-full py-3 px-4 rounded-md shadow bg-indigo-600 text-white font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm ${loading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>

        {loading && (
          <div className="mt-8 p-6 bg-blue-50 rounded-md border border-blue-200 text-center">
            <div className="flex flex-col items-center space-y-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              <div>
                <p className="text-lg font-semibold text-gray-800">Deep Search in Progress</p>
                <p className="text-sm text-gray-600 mt-1">Breaking down your question, searching the web, and synthesizing findings...</p>
                <p className="text-xs text-gray-500 mt-2">This may take 15-30 seconds</p>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-8 p-4 bg-red-50 rounded-md border border-red-200 text-red-700 text-center">
            {error}
          </div>
        )}

        <ResultDisplay result={result} />
      </div>
    </div>
  );
}

export default App;

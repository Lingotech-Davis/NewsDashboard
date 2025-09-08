'use client'

import { useState } from 'react';
import BiasResult from '@/components/biasPage';

export default function BiasPage() {
  const [link, setLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!link.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch('http://localhost:8000/api/v1/bias/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: link }),
      });

      if (!res.ok) throw new Error(`Server responded with ${res.status}`);
      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      setError('Failed to analyze article. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100">Bias Detector</h1>
      <p className="mb-6 text-gray-700 dark:text-gray-300">
        Paste a link to a news article below. We'll analyze it for bias.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input
          type="url"
          placeholder="https://example.com/article"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded text-white transition ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {error && <p className="mt-6 text-red-600">{error}</p>}

      {result && <BiasResult result={result} />}

    </div>
  );
}

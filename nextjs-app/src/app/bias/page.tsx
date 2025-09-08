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
        body: JSON.stringify({
          url: link,
          priors: { left: 0.25, center: 0.5, right: 0.25 },
          thresholds: { claims: 0.5, left: 0.9, center: 0.5, right: 0.5 },
          weights: { prior: 3.0, source: 1.60, sentence: 0.025, article: 5.0 }
        }),
      });
      // Recommended approach for tuning:
      // 1) Open up 3 articles from all politically leaning sources (left, center, right)
      // 2) Read the article and determine for yourself if it's biased
      // 3) Feed the article into the model, determine if it's correct
      // 4) Determine what kind of error is happening (wrong model prediction, too heavy weighting, etc...)
      // 5) Adjust the weights accordingly

      // If fetch succeeds but backend returns error status
      if (!res.ok) {
        const errorText = await res.text(); // optional: parse error message
        throw new Error(`Backend error: ${res.status} ${errorText}`);
      }

      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      if (err.name === 'TypeError' && err.message.includes('Failed to fetch')) {
        setError('Unable to connect to backend. Is the server running?');
      } else if (err.message.startsWith('Backend error')) {
        setError('Server responded with an error. Please check the article link or try a different URL.');
      } else {
        setError('Unexpected error occurred. Please try again or check server connection.');
      }
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

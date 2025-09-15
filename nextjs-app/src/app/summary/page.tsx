'use client'

import { useState } from 'react';
import ArticleSummaryResult from '@/components/summaryPage';

export default function SummaryPage() {
  const [link, setLink] = useState('');
  const [sentenceCount, setSentenceCount] = useState<number>(3);
  const [mode, setMode] = useState<'nlp' | 'ai'>('nlp'); // new state for mode
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!link.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const endpoint =
      mode === 'nlp'
        ? 'http://localhost:8000/api/v1/summarize/analyze'
        : 'http://localhost:8000/api/v1/summarize/generate';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: link,
          sentences: sentenceCount,
        }),
      });

      if (!res.ok) {
        const errorText = await res.text();
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
      <h1 className="text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100">Summarizer</h1>
      <p className="mb-6 text-gray-700 dark:text-gray-300">
        Paste a link to a news article below. Choose your summarization method.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <div className="flex space-x-4">
          <input
            type="url"
            placeholder="https://example.com/article"
            value={link}
            onChange={(e) => setLink(e.target.value)}
            className="flex-1 border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            required
          />

          <input
            type="number"
            min={1}
            max={20}
            value={sentenceCount}
            onChange={(e) => setSentenceCount(Number(e.target.value))}
            className="w-24 border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            placeholder="#"
          />
        </div>

        <div className="flex items-center space-x-4">
          <label className="text-sm text-gray-700 dark:text-gray-300">Method:</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value as 'nlp' | 'ai')}
            className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          >
            <option value="nlp">NLP (extractive summarization algorithm)</option>
            <option value="ai">AI (uses Gemini API calls)</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded text-white transition ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'Summarizing...' : 'Summarize'}
        </button>

        {error && <p className="mt-6 text-red-600">{error}</p>}
        {result && <ArticleSummaryResult result={result} />}
      </form>
    </div>
  );
}

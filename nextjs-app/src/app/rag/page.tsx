"use client"

import { useState, useEffect } from "react";

import type { ragArticle } from '@/types/ragSnippetProps';
import RagSnippet from "@/components/ragSnippet";


export default function NewsPage() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);


  if (error) return <div>{error}</div>;

  const startAnalysis = async (query: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`http://localhost:8000/api/v1/rag/rag-response-full-articles/?query=${encodeURIComponent(query)}`, {
        method: 'POST',
        // Remove headers and body as the data is now in the URL
      });

      // If fetch succeeds but backend returns error status
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    startAnalysis(query);
  };

  const renderMarkdown = (text: string) => {
    if (!text) return '';
    // Replace **bold** with <strong>bold</strong>
    const htmlString = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return { __html: htmlString };
  };


  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100">Retrieval Augmented Generation</h1>
      <p className="mb-6 text-gray-700 dark:text-gray-300">
        Enter a question to have answered by our RAG system.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input
          placeholder="How has AI impacted student learning and education?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded text-white transition ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
            }`}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {error && <p className="mt-6 text-red-600">{error}</p>}

      {result && (
        <>
          <div className="mt-8">
            <div className="p-6 rounded-lg border bg-gray-50 dark:bg-gray-800 dark:text-white shadow">
              <h3 className="text-xl font-semibold mb-2">Generated Summary using relevant sources</h3>
              <div className="p-4 border rounded bg-white dark:bg-gray-900">
                <p
                  className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap"
                  dangerouslySetInnerHTML={renderMarkdown(result.gemini_response)}
                ></p>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="text-xl font-semibold mb-4">Sources</h3>
              <div className="space-y-6">
                {result.articles.map((article: ragArticle, i: number) => (
                  <RagSnippet {...article} key={i} index={i} />
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

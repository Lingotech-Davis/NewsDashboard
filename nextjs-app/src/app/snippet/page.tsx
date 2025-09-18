"use client"

import { useState, useEffect } from "react";
import NewsCard from "@/components/newsSnippet";

import type { NewsSnippetProps } from '@/types/newsSnippetProps';
import NewsSnippet from "@/components/newsSnippet";


export default function NewsPage() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchNews() {
      setLoading(true);
      try {
        const res = await fetch("http://localhost:8000/api/v1/rag/retrieve-relevant-chunks-cosine/?query=" + query);
        console.log(res);
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
    }
    fetchNews();
  }, [query]);

  if (error) return <div>{error}</div>;


  return (
    <div className=" max-w-4xl mx-auto">
      <div className="max-w-2xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100">Snippet Finder</h1>
        <p className="mb-6 text-gray-700 dark:text-gray-300">
          Please enter a query below, and we'll find similar relevant entries in our news database.
        </p>
        <div className="flex flex-col space-y-4">
          <input
            type="url"
            placeholder="How is the S&amp;P reacting to Elon Musk antics"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            required
          />
        </div>
      </div>


      {error && <p className="mt-6 text-red-600">{error}</p>}

      {result && result.length > 0 && (
        <ul className="space-y-4 mt-4">
          {result.map((chunk: NewsSnippetProps, i: number) => (
            <NewsSnippet key={chunk.chunk_id} {...chunk} index={i} />
          ))}
        </ul>
      )}
    </div>

  );
}

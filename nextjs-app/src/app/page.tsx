"use client"

import { useState, useEffect } from "react";
import NewsCard from "@/components/newsCard";
import SearchPanel from "@/components/searchPanel";

import type { NewsApiResponse } from '@/types/newsResponse';


export default function NewsPage() {
  const [data, setData] = useState<NewsApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  // const [live, setLive] = useState<boolean>(false);

  useEffect(() => {
    async function fetchNews() {
      try {
        const res = await fetch("/api/news/file");
        console.log(res);
        const json = await res.json();
        if (!json.success) throw new Error("API responded with failure");
        setData(json.data);
      } catch (err) {
        setError("Failed to load news.");
        console.log(err);
      }
    }
    fetchNews();
  }, []);

  if (error) return <div>{error}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Latest News</h2>
      <SearchPanel setData={setData} />
      <ul className="space-y-4">
        {data.articles.map((article, i) => (
          <NewsCard key={i} article={article} index={i} />
        ))}
      </ul>
    </div>
  );
}

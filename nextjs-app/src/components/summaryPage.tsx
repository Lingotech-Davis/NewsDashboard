'use client';

import React, { useState } from 'react';

type ArticleSummaryProps = {
  result: {
    summary: string[];
    extra: {
      title: string;
      authors: string[];
      publish_date: string;
      text: string;
      source: string;
    };
  };
};

export default function ArticleSummaryResult({ result }: ArticleSummaryProps) {
  const { summary, extra } = result;
  const [showFullArticle, setShowFullArticle] = useState(false);

  return (
    <div className="mt-8 p-6 rounded-lg border bg-gray-50 dark:bg-gray-800 dark:text-white shadow">
      <h2 className="text-2xl font-semibold mb-2">{extra.title}</h2>
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
        Source: <span className="font-medium">{extra.source}</span> | Published:{' '}
        <span className="font-medium">{extra.publish_date}</span>
      </p>

      <h3 className="text-lg font-semibold h-8">Summary</h3>

      <div className="max-h-[600px] overflow-y-auto p-4 border rounded bg-white dark:bg-gray-900 space-y-2">
        {summary.map((sent, idx) => {
          const sentence_background = 'bg-transparent';
          return (
            <div key={idx} className={`p-2 rounded ${sentence_background}`}>
              <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                {sent}
              </p>
            </div>
          );
        })}
      </div>
      <div className="flex items-center mb-2 text-sm text-yellow-700 dark:text-yellow-300 bg-yellow-50 dark:bg-yellow-900 border-l-4 border-yellow-500 px-3 py-2 rounded mt-6">
        ⚠️ <span className="ml-2">This article summary is generated automatically and may omit key context.</span>
      </div>
    </div>
  );
}

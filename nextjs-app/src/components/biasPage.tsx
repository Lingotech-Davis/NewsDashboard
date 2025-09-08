import React from 'react';

type BiasResultProps = {
  result: {
    title: string;
    source: string;
    bias_prediction: string;
    bias_distribution: {
      left: number;
      center: number;
      right: number;
    };
    article_summary: {
      authors: string[];
      publish_date: string;
      text_snippet: string;
    };
  };
};

export default function BiasResult({ result }: BiasResultProps) {
  const { title, source, bias_prediction, bias_distribution, article_summary } = result;

  return (
    <div className="mt-8 p-6 rounded-lg border bg-gray-50 dark:bg-gray-800 dark:text-white shadow">
      <h2 className="text-2xl font-semibold mb-2">{title}</h2>
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
        Source: <span className="font-medium">{source}</span> | Predicted Bias: <span className="font-bold capitalize">{bias_prediction}</span>
      </p>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Bias Distribution</h3>
        <ul className="space-y-1">
          {Object.entries(bias_distribution).map(([key, value]) => (
            <li key={key} className="flex justify-between">
              <span className="capitalize">{key}</span>
              <span>{(value * 100).toFixed(2)}%</span>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Article Summary</h3>
        <p className="text-sm text-gray-700 dark:text-gray-200 mb-2">
          <strong>Published:</strong> {new Date(article_summary.publish_date).toLocaleString()}
        </p>
        <p className="text-sm text-gray-700 dark:text-gray-200 mb-2">
          <strong>Authors:</strong> {article_summary.authors.join(', ')}
        </p>
        <p className="text-sm text-gray-700 dark:text-gray-200 whitespace-pre-wrap">
          <strong>Snippet:</strong> {article_summary.text_snippet}
        </p>
      </div>
    </div>
  );
}

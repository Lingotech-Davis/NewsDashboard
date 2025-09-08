import React from 'react';

type BiasResultProps = {
  result: {
    title: string;
    source: string;
    source_bias: string;
    bias_prediction: string;
    bias_distribution: {
      left: number;
      center: number;
      right: number;
    };
    article_summary: {
      authors: string[];
      publish_date: string;
      text: string;
    };
  };
};

export default function BiasResult({ result }: BiasResultProps) {
  const { title, source, source_bias, bias_prediction, bias_distribution, article_summary } = result;

  return (
    <div className="mt-8 p-6 rounded-lg border bg-gray-50 dark:bg-gray-800 dark:text-white shadow">
      <h2 className="text-2xl font-semibold mb-2">{title}</h2>
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
        Source: <span className="font-medium">{source}</span> | Source Bias: <span className="font-bold capitalize">{source_bias}</span>
      </p>

    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-2">Article Bias Distribution</h3>
      <div className="space-y-3">
        {Object.entries(bias_distribution).map(([label, value]) => {
          const percent = (value * 100).toFixed(2);
          const color =
            label === 'left' ? 'bg-blue-500' :
            label === 'center' ? 'bg-gray-500' :
            label === 'right' ? 'bg-red-500' : 'bg-gray-300';

          return (
            <div key={label}>
              <div className="flex justify-between text-sm mb-1">
                <span className="capitalize">{label}</span>
                <span>{percent}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded h-4">
                <div
                  className={`${color} h-4 rounded`}
                  style={{ width: `${percent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
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
          <strong>Text:</strong> {article_summary.text}
        </p>
      </div>
    </div>
  );
}

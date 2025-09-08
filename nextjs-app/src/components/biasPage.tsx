'use client';

import React, { useState } from 'react';

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
    sentence_predictions: {
      index: number;
      text: string;
      probs: {
        left: number;
        center: number;
        right: number;
      };
      label: string;
      is_claim: boolean;
    }[];
    extra: {
      match: string;
      article_probs: {
        left: number;
        center: number;
        right: number;
      };
      source_probs: {
        left: number;
        center: number;
        right: number;
      };
      per_political: number;
      url: string;
    };
  };
};

export default function BiasResult({ result }: BiasResultProps) {
  const {
    title,
    source,
    source_bias,
    bias_prediction,
    bias_distribution,
    article_summary,
    sentence_predictions,
    extra,
  } = result;

  const [showClaimsOnly, setShowClaimsOnly] = useState(false);

  const labelColor = {
    left: 'text-blue-600',
    center: 'text-gray-600',
    right: 'text-red-600',
  };
  const biasBackground = {
  left: 'bg-blue-100 dark:bg-blue-900 border-l-4 border-blue-500',
  center: 'bg-gray-100 dark:bg-gray-800 border-l-4 border-gray-500',
  right: 'bg-red-100 dark:bg-red-900 border-l-4 border-red-500',
  };

  return (
    <div className="mt-8 p-6 rounded-lg border bg-gray-50 dark:bg-gray-800 dark:text-white shadow">
      <h2 className="text-2xl font-semibold mb-2">{title}</h2>
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
        Source: <span className="font-medium">{source}</span> | Source Bias:{' '}
        <span className="font-bold capitalize">{source_bias}</span>
      </p>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Article Bias Distribution</h3>
        <div className="space-y-3">
          {Object.entries(bias_distribution).map(([label, value]) => {
            const percent = (value * 100).toFixed(2);
            const color =
              label === 'left'
                ? 'bg-blue-500'
                : label === 'center'
                ? 'bg-gray-500'
                : label === 'right'
                ? 'bg-red-500'
                : 'bg-gray-300';

            return (
              <div key={label}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize">{label}</span>
                  <span>{percent}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded h-4">
                  <div className={`${color} h-4 rounded`} style={{ width: `${percent}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {sentence_predictions && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold">Smart Reader</h3>
          <div className="mb-4">
            <label className="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                checked={showClaimsOnly}
                onChange={() => setShowClaimsOnly(!showClaimsOnly)}
                className="form-checkbox h-4 w-4 text-blue-600"
              />
              <span>Show claims only</span>
            </label>
          </div>

          <div className="max-h-[600px] overflow-y-auto p-4 border rounded bg-white dark:bg-gray-900 space-y-2">
            {sentence_predictions
              .filter((sent) => !showClaimsOnly || sent.is_claim)
              .map((sent) => {
                const claimClass = sent.is_claim
                  ? 'bg-green-100 dark:bg-green-800 border-l-4 border-green-500'
                  : 'bg-transparent';

                return (
                  <div key={sent.index} className={`p-2 rounded ${claimClass}`}>
                    <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                      {sent.text}
                    </p>
                    <div className="text-xs text-gray-600 dark:text-gray-300 mt-1">
                      <span className="font-semibold">
                        {sent.is_claim ? 'Claim' : 'Not a Claim'}
                      </span>
                    </div>
                  </div>
                );
              })}
          </div>
          <div className="flex items-center mb-2 text-sm text-yellow-700 dark:text-yellow-300 bg-yellow-50 dark:bg-yellow-900 border-l-4 border-yellow-500 px-3 py-2 rounded mt-6">
              ⚠️ <span className="ml-2">Sentence-level predictions are experimental and may not be fully accurate.</span>
          </div>
        </div>
      )}
    </div>
  );
}

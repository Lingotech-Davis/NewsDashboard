'use client';

import type { ragArticle } from "@/types/ragSnippetProps";
import Image from "next/image";
import Link from "next/link";



export default function RagSnippet({ index, url, urlToImage, author, text, title }: ragArticle) {
  const truncateString = (text: string, maxLength: number) => {
    return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
  };

  return (
    <li className="flex flex-col sm:flex-row gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-[#111] shadow-sm transition hover:shadow-md">
      {/* Thumbnail */}
      <div className="w-full sm:w-48 h-48 relative flex-shrink-0">
        {urlToImage ? (
          <img
            src={urlToImage}
            alt="News thumbnail"
            className="object-cover w-full h-full rounded-lg"
          />
        ) : (
          <>
            <Image
              src="/no_image_dark.svg"
              fill
              alt="No image"
              className="object-contain dark:hidden"
            />
            <Image
              src="/no_image_light.svg"
              fill
              alt="No image"
              className="object-contain hidden dark:block"
            />
          </>
        )}
      </div>

      {/* Text content */}
      <div className="flex flex-col justify-between flex-grow">
        <div>
          <h3 className="text-lg font-semibold mb-1">
            {index != null ? `${index + 1}. ` : ""}
            <a href={url} target="_blank" rel="noopener noreferrer" className="hover:underline">
              {title}
            </a>
          </h3>
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {truncateString(text, 500)}
          </p>
        </div>
        <div className="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400 mt-2">
          <span>Source: {author}</span>
          <Link
            href={`/bias?url=${encodeURIComponent(url)}`}
            className="text-blue-500 hover:text-blue-700 font-medium"
          >
            Analyze Bias
          </Link>
        </div>
      </div>
    </li>
  );
}

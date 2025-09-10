'use client';

import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="w-full flex justify-end p-4 border-b border-gray-200 dark:border-gray-500 rounded-xl bg-white dark:bg-[#111] shadow-sm">
      <ul className="flex space-x-6">
        <li>
          <Link href="/">
            <span className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">Home</span>
          </Link>
        </li>
        <li>
          <Link href="/bias">
            <span className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">Bias Detector</span>
          </Link>
        </li>
        <li>
          <Link href="/rag">
            <span className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">Snippet Finder</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
}

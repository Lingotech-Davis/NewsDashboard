'use client';

import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="w-full flex justify-end p-4 bg-gray-100 shadow">
      <ul className="flex space-x-6">
        <li>
          <Link href="/bias">
            <span className="text-blue-600 hover:underline cursor-pointer">Bias Detector</span>
          </Link>
        </li>
        <li>
          <Link href="/">
            <span className="text-blue-600 hover:underline cursor-pointer">Home</span>
          </Link>
        </li>
        <li>
          <span className="text-gray-500 cursor-not-allowed">Coming Soon</span>
        </li>
      </ul>
    </nav>
  );
}

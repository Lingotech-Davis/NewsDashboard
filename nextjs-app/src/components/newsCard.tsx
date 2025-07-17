import type { NewsCardProps } from "@/types/newsCardProps";
import Image from "next/image";

export default function NewsCard({ article, index }: NewsCardProps) {
	return (
		<li className="flex flex-col sm:flex-row gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-[#111] shadow-sm transition hover:shadow-md">
			{/* Thumbnail */}
			<div className="w-full sm:w-48 h-48 relative flex-shrink-0">
				{article.urlToImage ? (
					<img
						src={article.urlToImage}
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
						<a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
							{article.title}
						</a>
					</h3>
					<p className="text-sm text-gray-700 dark:text-gray-300">
						{article.description}
					</p>
				</div>
				<p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
					Source: {article.source.name}
				</p>
			</div>
		</li>
	);
}

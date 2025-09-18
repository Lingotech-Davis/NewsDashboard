
export interface ragArticle {
	url: string;
	urlToImage: string | null;
	author: string | null;
	description: string;
	scrape_successful: string;
	source: string;
	article_id: string;
	title: string;
	publishedAt: string; // Note: This is an ISO 8601 string.
	text: string;
	index: number;
}


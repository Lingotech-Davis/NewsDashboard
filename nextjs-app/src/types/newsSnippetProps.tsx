import type { Article } from "./newsResponse";

export interface RagArticleRead {
	url: string;
	urlToImage: string | null;
	source: string;
	author: string | null;
	title: string;
	publishedAt: string;
}

export interface NewsSnippetProps {
	article: RagArticleRead;
	chunk_id: string;
	content: string;
	created_at: string; // iso
	article_id: string;
	index?: number;
}

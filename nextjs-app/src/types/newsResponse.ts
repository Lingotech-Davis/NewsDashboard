export interface NewsApiResponse {
  status: string;
  totalResults: number;
  articles: Article[];
}

export interface Article {
  source: Source;
  author: string | null;
  title: string;
  description: string | null;
  url: string;
  urlToImage: string | null;
  publishedAt: string; // ISO date string
  content: string | null;
}

export interface Source {
  id: string | null;
  name: string;
}

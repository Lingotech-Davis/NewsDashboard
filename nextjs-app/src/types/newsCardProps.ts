import type { Article } from "./newsResponse";

export interface NewsCardProps {
  article: Article;
  index?: number;
}

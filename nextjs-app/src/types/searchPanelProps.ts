import type { NewsApiResponse } from "./newsResponse";

export interface SearchPanelProps {
  setData: (data: NewsApiResponse) => void;
}

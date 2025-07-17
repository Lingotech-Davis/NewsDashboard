import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const endpoint = searchParams.get("endpoint") || "top-headlines";

  const validEndpoints = ["top-headlines", "everything"];
  if (!validEndpoints.includes(endpoint)) {
    return Response.json({ error: "Invalid endpoint" }, { status: 400 });
  }

  const opts_top = ["country", "category", "sources", "q", "language"];
  // qInTitle not documented but is sufficient
  const opts_every = [
    "q",
    "qInTitle",
    "searchIn",
    "sources",
    "domains",
    "excludeDomains",
    "from",
    "to",
    "language",
    "sortBy",
  ];
  const req_opts_every = ["q", "qInTitle", "sources", "domains"];

  const allowedOptions = endpoint === "top-headlines" ? opts_top : opts_every;

  const params: Record<string, string> = {};
  for (const opt of allowedOptions) {
    const value = searchParams.get(opt);
    if (value) params[opt] = value;
  }

  // determine behavior, fail or fix silently?
  if (endpoint === "top-headlines" && !opts_top.some((key) => key in params)) {
    params.country = "us"; // fallback
  }

  if (
    endpoint === "everything" &&
    !req_opts_every.some((key) => key in params)
  ) {
    params.q = "stocks"; // fallback
  }

  const apiKey = process.env.NEWS_API_KEY;
  if (!apiKey) {
    return Response.json({ error: "Missing API key" }, { status: 500 });
  }

  const paramStr = new URLSearchParams({ ...params, apiKey }).toString();
  const url = `https://newsapi.org/v2/${endpoint}?${paramStr}`;

  const res = await fetch(url);
  if (!res.ok) {
    return Response.json(
      { error: "NewsAPI failed", status: res.status },
      { status: 502 },
    );
  }

  const data = await res.json();
  return Response.json(data, { status: 200 });
}

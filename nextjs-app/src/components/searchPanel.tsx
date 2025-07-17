'use client'

import * as Popover from "@radix-ui/react-popover";
import * as Switch from "@radix-ui/react-switch";

import { useState } from "react";
import type { SearchPanelProps } from "@/types/searchPanelProps";
import { CategorySelect } from "./categorySelect";
import Image from "next/image";

export default function SearchPanel({ setData }: SearchPanelProps) {
	const [query, setQuery] = useState<string>("");
	const [top, setTop] = useState<boolean>(true)
	const [category, setCategory] = useState('none')

	// One of the following needs to be filled out for a valid API call to be made
	// const req_opts_top = ["country", "category", "sources", "q", "language"];
	// const req_opts_every = ["q", "qInTitle", "sources", "domains"];
	// const categories = ["business", 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

	async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
		e.preventDefault()

		if (!query && category === 'none') {
			console.warn('Nothing selected: must provide query or category')
			alert('You must provide a query or category');
			return
		}

		const params: Record<string, string> = {
			endpoint: top ? 'top-headlines' : 'everything',
			q: query,
		}
		if (category != 'none') {
			params["category"] = category
		}

		const paramStr = new URLSearchParams({ ...params }).toString();
		const url = `/api/news/live?${paramStr}`;

		const res = await fetch(url);
		if (!res.ok) {
			console.error(`API call failed with status ${res.status}`);
			return;
		}

		const data = await res.json();
		setData(data);
		console.log(data);
	}

	return (
		<div >
			<form className="flex w-full pb-4" onSubmit={handleSubmit}>
				<input className="border-1 border-gray-200 dark:border-gray-700 rounded-md" value={query} onChange={(e) => setQuery(e.target.value)} />
				<Popover.Root>
					<Popover.Trigger asChild>
						<img className="clickable" src="/wrench.svg" width={30} />
					</Popover.Trigger>
					<Popover.Portal>
						<Popover.Content
							className="z-20 rounded p-4 w-[500px] bg-white dark:bg-[#111] border-2 border-gray-200 dark:border-gray-700"
							sideOffset={5}
						>
							<div className="flex flex-col gap-2.5">
								<p className="text-[15px] font-medium mb-2.5">API Endpoint Settings</p>
								<div style={{ display: "flex", alignItems: "center" }}>
									<label
										className="Label"
										htmlFor="airplane-mode"
										style={{ paddingRight: 15 }}
									>
										Everything
									</label>
									<Switch.Root
										id="Hitting the 'top headlines' endpoint"
										checked={top}
										onCheckedChange={setTop}
										className="w-11 h-6 bg-gray-300 dark:bg-gray-700 rounded-full relative data-[state=checked]:bg-blue-600 transition-colors"
									>
										<Switch.Thumb
											className="block w-5 h-5 bg-white rounded-full shadow-md translate-x-1 transition-transform data-[state=checked]:translate-x-5"
										/>
									</Switch.Root>
									<label
										className="Label"
										htmlFor="airplane-mode"
										style={{ paddingLeft: 15 }}
									>
										Top Headlines
									</label>
								</div>
								{/* {TAGS.map((item, index) => ( */}
								{/*   <fieldset className="flex gap-5 items-center" key={index}> */}
								{/*     <label className="text-[13px] w-[90px]" htmlFor={item}> */}
								{/*       {item} */}
								{/*     </label> */}
								{/*     <input */}
								{/*       type="checkbox" */}
								{/*       className="w-full inline-flex items-center justify-center flex-1 rounded px-2.5 text-[13px] leading-none h-[25px]" */}
								{/*       id={item} */}
								{/*       checked={tagFilter[index]} */}
								{/*       onChange={() => {handleClick(index)}} */}
								{/*     /> */}
								{/*   </fieldset> */}
								{/* ))} */}
								<CategorySelect value={category} onValueChange={setCategory} />
							</div>
							<Popover.Close
								className="inline-flex items-center justify-center absolute top-[10px] right-[10px]"
								aria-label="Close"
							>
								{/* <img src="assets/exit.svg" /> */}
								<>
									<Image
										src="/exit_dark.svg"
										width={10} height={10}
										alt="No image"
										className="object-contain dark:hidden"
									/>
									<Image
										src="/exit_light.svg"
										width={10} height={10}
										alt="No image"
										className="object-contain hidden dark:block"
									/>
								</>
							</Popover.Close>
							<Popover.Arrow className="fill-white" />
						</Popover.Content>
					</Popover.Portal>
				</Popover.Root>
				<button
					type="submit"
					className="px-3 py-1.5 text-sm rounded-md bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-500 dark:hover:bg-blue-600 transition-colors"
				>
					Submit
				</button></form>
		</div>
	)
}



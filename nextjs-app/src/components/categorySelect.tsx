'use client'

import * as React from 'react'
import * as Select from '@radix-ui/react-select'
import {
	ChevronDownIcon,
	ChevronUpIcon,
	CheckIcon,
} from '@radix-ui/react-icons'

const categories = [
	'NONE',
	'business',
	'entertainment',
	'general',
	'health',
	'science',
	'sports',
	'technology',
]

function classnames(...classes: (string | false | null | undefined)[]) {
	return classes.filter(Boolean).join(' ')
}

export function CategorySelect({
	value,
	onValueChange,
}: {
	value: string
	onValueChange: (val: string) => void
}) {
	return (
		<Select.Root value={value} onValueChange={onValueChange}>
			<Select.Trigger
				className="inline-flex items-center justify-between rounded-md px-3 py-2 bg-white dark:bg-neutral-900 text-black dark:text-white border border-gray-300 dark:border-neutral-700 text-sm w-[200px]"
				aria-label="Category"
			>
				<Select.Value placeholder="Select a category" />
				<Select.Icon>
					<ChevronDownIcon className="text-gray-500 dark:text-gray-400" />
				</Select.Icon>
			</Select.Trigger>
			<Select.Portal>
				<Select.Content
					className="z-30 overflow-hidden rounded-md bg-white dark:bg-neutral-900 border border-gray-300 dark:border-neutral-700 shadow-lg"
					sideOffset={5}
				>
					<Select.ScrollUpButton className="flex items-center justify-center h-6 text-gray-500">
						<ChevronUpIcon />
					</Select.ScrollUpButton>
					<Select.Viewport className="p-1">
						{categories.map((cat) => (
							<SelectItem key={cat} value={cat.toLowerCase()}>
								{cat}
							</SelectItem>
						))}
					</Select.Viewport>
					<Select.ScrollDownButton className="flex items-center justify-center h-6 text-gray-500">
						<ChevronDownIcon />
					</Select.ScrollDownButton>
				</Select.Content>
			</Select.Portal>
		</Select.Root>
	)
}

const SelectItem = React.forwardRef<
	HTMLDivElement,
	React.ComponentPropsWithoutRef<typeof Select.Item>
>(({ children, className, ...props }, forwardedRef) => {
	return (
		<Select.Item
			className={classnames(
				'text-sm cursor-pointer select-none rounded px-2 py-1.5 text-black dark:text-white focus:outline-none focus:bg-gray-100 dark:focus:bg-neutral-800 flex items-center justify-between',
				className
			)}
			{...props}
			ref={forwardedRef}
		>
			<Select.ItemText>{children}</Select.ItemText>
			<Select.ItemIndicator className="ml-2 text-blue-500">
				<CheckIcon />
			</Select.ItemIndicator>
		</Select.Item>
	)
})
SelectItem.displayName = 'SelectItem'

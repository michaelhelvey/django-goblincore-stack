import { render } from 'preact'
import { useState } from 'preact/hooks'

function App() {
	const [count, setCount] = useState(0)

	return (
		<div className="mt-5 flex flex-col p-5 border border-gray-300 rounded">
			<div className="font-bold text-2xl">My Preact App:</div>
			<p className="my-3">Count: {count}</p>
			<button className="button" onClick={() => setCount(count + 1)}>
				Inc
			</button>
		</div>
	)
}

// On intial page load, render the app
render(<App />, document.getElementById('app')!)

// Also render the app on subsequent "turbo" loads:
document.addEventListener('turbo:load', () => {
	render(<App />, document.getElementById('app')!)
})

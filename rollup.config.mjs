import nodeResolve from '@rollup/plugin-node-resolve'
import { join } from 'path'
import esbuild from 'rollup-plugin-esbuild'

const STATIC_PATH = join('app', 'static')
const JS_PATH = join('app', 'static', 'js')
const buildDir = fileType => join(STATIC_PATH, 'build', fileType)

export default [
	{
		input: join(JS_PATH, 'global/index.ts'),
		output: {
			file: join(buildDir('js'), 'global.js'),
			format: 'es',
			sourcemap: true,
		},
		plugins: [
			nodeResolve(),
			esbuild({ minify: process.env.NODE_ENV === 'production', sourceMap: true }),
		],
	},
]

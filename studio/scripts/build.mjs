import {build} from 'vite';
await import('./sync-data.mjs');
await build({configFile:false,base:'./',esbuild:{jsx:'automatic'}});

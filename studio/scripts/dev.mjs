import {createServer} from 'vite';
const server=await createServer({configFile:false,base:'./',esbuild:{jsx:'automatic'},server:{host:'127.0.0.1'}});
await server.listen();server.printUrls();

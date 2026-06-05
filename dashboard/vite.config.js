// Dashboard for IPA27 Project
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'

function serveResultsData() {
  return {
    name: 'serve-results-data',
    configureServer(server) {
      server.middlewares.use('/IPA27_project/data', (req, res, next) => {
        const filePath = path.resolve(__dirname, '../../results/data', req.url.slice(1).split('?')[0]);
        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
          const ext = path.extname(filePath);
          if (ext === '.json') res.setHeader('Content-Type', 'application/json');
          else if (ext === '.xlsx') res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
          else if (ext === '.csv') res.setHeader('Content-Type', 'text/csv');
          res.end(fs.readFileSync(filePath));
        } else {
          next();
        }
      });
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    serveResultsData()
  ],
  base: '/IPA27_project/',
})

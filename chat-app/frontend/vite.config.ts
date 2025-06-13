import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import path from "path"
import {TanStackRouterVite} from "@tanstack/router-plugin/vite"

export default defineConfig({
  plugins: [react(), tailwindcss(), TanStackRouterVite({target: 'react', autoCodeSplitting: true}) ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
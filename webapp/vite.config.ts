import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/verbaterra.github.io/",
  plugins: [react()],
});

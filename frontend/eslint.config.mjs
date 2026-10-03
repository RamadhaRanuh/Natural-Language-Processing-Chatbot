import js from "@eslint/js";
import tseslint from "typescript-eslint";
import hooks from "eslint-plugin-react-hooks";

export default tseslint.config(
  { ignores: [".next/**", "node_modules/**", "next-env.d.ts", "playwright-report/**", "test-results/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { files: ["scripts/*.mjs"], languageOptions: { globals: { window: "readonly" } } },
  {
    files: ["**/*.ts", "**/*.tsx"],
    plugins: { "react-hooks": hooks },
    rules: { ...hooks.configs.recommended.rules },
  }
);

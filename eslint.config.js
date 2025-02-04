export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest"
    },
    rules: {
      "semi": ["error", "always"],
      "quotes": ["error", "double"],
      "indent": ["error", 2],
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];

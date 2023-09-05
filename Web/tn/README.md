## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
   parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
   },
```

- Replace `plugin:@typescript-eslint/recommended` to `plugin:@typescript-eslint/recommended-type-checked` or `plugin:@typescript-eslint/strict-type-checked`
- Optionally add `plugin:@typescript-eslint/stylistic-type-checked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and add `plugin:react/recommended` & `plugin:react/jsx-runtime` to the `extends` list

npm create vite@latest
## Used Packages (in case you need)

npm install axios (REST API)
npm install uuid (To generate random numbers for unique file names)
npm install react-firebase-hooks
npm install firebase
npm install react-router-dom

?pip3 install Flask?

## src/Config/firebase.ts => Update firebase informations before using

## Next to work on: Connect src/Backend/main.py => Flask and src/Pages/translator.tsx => Axios
## Create the rest API, update sendData function
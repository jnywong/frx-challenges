const path = require("path");
const webpack = require("webpack");
const autoprefixer = require("autoprefixer");
const miniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  context: __dirname,
  entry: "./static/web/index.js",
  output: {
    path: path.resolve(__dirname, "static/webpack-output/"),
    publicPath: "auto", // necessary for CDNs/S3/blob storages
    filename: "[name].js",
  },
  plugins: [new miniCssExtractPlugin()],
  module: {
    rules: [
      {
        test: /\.(scss)$/,
        use: [
          {
            loader: miniCssExtractPlugin.loader,
          },
          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: "css-loader",
          },
          {
            // Loader for webpack to process CSS with PostCSS
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [autoprefixer],
              },
            },
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: "sass-loader",
          },
        ],
      },
      {
        test: /\.css$/i,
        use: [miniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
};

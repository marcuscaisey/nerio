const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  mode: "production",
  entry: {
    "js/base": "./js/base.js",
    "js/home": "./js/home.js",
    "css/styles": "./sass/styles.scss",
  },
  output: {
    path: path.resolve(__dirname, "static"),
    filename: "[name].js",
  },
  plugins: [new MiniCssExtractPlugin()],
  module: {
    rules: [
      {
        test: /\.js$/,
        include: path.resolve(__dirname, "./js"),
        loader: "babel-loader",
        options: {
          plugins: ["@babel/plugin-proposal-class-properties"],
          presets: [
            [
              "@babel/preset-env",
              {targets: "defaults", useBuiltIns: "usage", corejs: 3},
            ],
          ],
        },
      },
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
    ],
  },
};

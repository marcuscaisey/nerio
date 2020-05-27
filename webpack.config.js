const path = require("path");
const srcPath = "./js/";

module.exports = {
  mode: "production",
  watch: true,
  entry: {
    base: srcPath + "base.js",
    home: srcPath + "home.js",
  },
  output: {
    path: path.resolve(__dirname, "static/js"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        include: [
          path.resolve(__dirname, srcPath),
        ],
        loader: "babel-loader",
        options: {
          plugins: [
            "@babel/plugin-proposal-class-properties",
          ],
          presets: [
            [
              "@babel/preset-env",
              {
                targets: "defaults",
                useBuiltIns: "usage",
                corejs: 3,
              },
            ],
          ],
        },
      },
    ],
  },
};
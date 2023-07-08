const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./wallet.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
  },
  resolve: {
    fallback: {
      stream: require.resolve("stream-browserify"),
      assert: require.resolve("assert/"),
      util: require.resolve("util/"),
      http: require.resolve("stream-http"),
      https: require.resolve("https-browserify"),
      url: require.resolve("url/"),
      os: require.resolve("os-browserify/browser"),
      buffer: require.resolve("buffer"),
    },
  },
  plugins: [
    // fix "process is not defined" error:
    new webpack.ProvidePlugin({
      process: "process/browser",
      Buffer: ["buffer", "Buffer"],
    }),
  ],
};

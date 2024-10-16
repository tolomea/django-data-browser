const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  webpack: function (config, env) {
    // Modify the output configuration
    config.output.filename = 'static/js/main.js';
    config.output.chunkFilename = 'static/js/[name].chunk.js';

    // Modify the MiniCssExtractPlugin configuration
    const miniCssExtractPlugin = config.plugins.find(
      plugin => plugin.constructor.name === 'MiniCssExtractPlugin'
    );
    if (miniCssExtractPlugin) {
      miniCssExtractPlugin.options.filename = 'static/css/main.css';
      miniCssExtractPlugin.options.chunkFilename = 'static/css/[name].chunk.css';
    }

    // Modify HtmlWebpackPlugin
    const htmlWebpackPlugin = config.plugins.find(
      plugin => plugin.constructor.name === 'HtmlWebpackPlugin'
    );
    if (htmlWebpackPlugin) {
      htmlWebpackPlugin.options.inject = false; // Prevent automatic injection
      htmlWebpackPlugin.options.template = path.resolve(__dirname, 'public', 'index.html');
    }

    return config;
  },
};
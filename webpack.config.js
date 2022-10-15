'use strict';

const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const argv = require('yargs').argv;
const bourbon = require('bourbon');

const shouldUseSourceMap = process.env.GENERATE_SOURCEMAP !== 'false';

const detectWebpackEnv = () => {
    const isProduction = process.NODE_ENV === 'production' || argv.production;
    const env = isProduction ? 'production' : 'development'
    process.env.BABEL_ENV = env;
    process.env.NODE_ENV = env;
    return env;
};

const configFactory = function (webpackEnv) {
  const isEnvDevelopment = webpackEnv === 'development';
  const isEnvProduction = webpackEnv === 'production';

  return {
    target: ['browserslist'],
    mode: isEnvProduction ? 'production' : isEnvDevelopment && 'development',
    // Stop compilation early in production
    bail: isEnvProduction,
    devtool: isEnvProduction
      ? shouldUseSourceMap
        ? 'source-map'
        : false
      : isEnvDevelopment && 'cheap-module-source-map',

    // Entry points locations.
    entry: {
        'regex-css': `${__dirname}/src/sass/screen.scss`,
    },
    // (Output) bundle locations.
    output: {
      // The build folder
      path: `${__dirname}/src/regex/static/bundles/`,
      // Add /* filename */ comments to generated require()s in the output.
      pathinfo: isEnvDevelopment,
      // no cache busting, Django takes care of that
      filename: '[name].js',
      chunkFilename: '[name].chunk.js',
      // webpack uses `publicPath` to determine where the app is being served from.
      // It requires a trailing slash, or the file assets will get an incorrect path.
      publicPath: '/static/bundles/',
    },

    optimization: {
      minimize: isEnvProduction,
    },

    // Plugins
    plugins: [
      new MiniCssExtractPlugin({
        // Options similar to the same options in webpackOptions.output
        // both options are optional
        filename: '[name].css',
      }),
    ],

    // How to build different types of modules
    module: {
      rules: [
        {
          test: /\.(scss|sass|css)$/,
          use: [
            {loader: MiniCssExtractPlugin.loader},
            {
              loader: 'css-loader',
              options: {
                url: false,
                importLoaders: 2,
                sourceMap: isEnvProduction
                  ? shouldUseSourceMap
                  : isEnvDevelopment,
                },
            },
            // Runs postcss configuration (postcss.config.js).
            {
              loader: 'postcss-loader'
            },
            {
              loader: 'sass-loader',
              options: {
                sassOptions: {
                  comments: !isEnvProduction,
                  includePaths: bourbon.includePaths,
                },
                sourceMap: true,
              }
            }
          ],
          // sideEffects: true,
        }
      ]
    }
  };
};


const webpackEnv = detectWebpackEnv();

/**
 * Webpack configuration
 * Run using "webpack" or "npm run build"
 */
module.exports = configFactory(webpackEnv);

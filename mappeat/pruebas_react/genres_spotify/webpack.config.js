var path = require('path');
var ROOT_PATH = path.resolve(__dirname);
var BUILD_PATH = path.join(ROOT_PATH, '/public/');

module.exports = {
    entry: './app/components/main.jsx',
    output: {
        path: BUILD_PATH,
        filename: "build.js",
    },
    module: {
        loaders: [
            {
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'react']
                }
            }
        ]
    }
};

var path = require('path');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    // This is the entry point to our javascript code
    entry: './app/index.js',
    // This is where to output the artifacts that
    // can be dropped into a web brower
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'index.js'
    },
    module: {
        rules: [
            // Use the babel loader for all .js files
            // We are specifically using it because we 
            // would like to use JSX syntax
            { test: /\.(js)$/, use: 'babel-loader' }
        ]
    },
    // Automatically generate an new html file that will include
    // all bundled assets 
    plugins: [
        new HtmlWebpackPlugin({ template: 'app/index.html' })
    ],
    mode: 'development'
};

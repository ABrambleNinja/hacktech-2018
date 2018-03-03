const path = require('path');

module.exports = {
    entry: './ui/main.js',  // main.js is where I plan to write the JSX code
    output: {
        path: path.resolve(__dirname, 'venv/static/js/'),
        filename: "main.js"
    },
    module: {
        rules: [
            { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
        ]
    }
}
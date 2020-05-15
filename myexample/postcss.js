#!/usr/bin/env node
let fs            = require('fs'),
    autoprefixer  = require('autoprefixer'),
    colorFunction = require('postcss-color-function'),
    cssvariables  = require('postcss-css-variables'),
    postcssImport = require('postcss-import'),
    postcss       = require('postcss'),
    args          = require('minimist')(process.argv);


if (!fs.existsSync(args.src)) {
    !process.exit(0);
}

let paths = (args.paths || '').split(',');

let plugins = [
    postcssImport({
        path: paths,
    }),
    cssvariables(),
    colorFunction(),
    autoprefixer(),
];

if (args.debug) {
    plugins = plugins.concat([
    ]);
} else {
    plugins = plugins.concat([
    ]);
}


fs.readFile(args.src, (err, css) => {
    postcss({plugins: plugins})
        .process(css, {from: args.src, to: args.dest})
        .then(result => {
            fs.writeFile(args.dest, result.css, () => true);
            if (result.map) {
                fs.writeFile(args.dest + '.map', result.map, () => true);
            }
        });
});

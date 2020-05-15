#!/usr/bin/env node
let cache,
    args          = require('minimist')(process.argv),
    fs            = require('fs'),
    commonjs      = require('rollup-plugin-commonjs'),
    html          = require('rollup-plugin-html'),
    includePaths  = require('rollup-plugin-includepaths'),
    json          = require('rollup-plugin-json'),
    node          = require('rollup-plugin-node-resolve'),
    postcss       = require('rollup-plugin-postcss'),
    rollup        = require('rollup'),
    colorFunction = require('postcss-color-function'),
    cssvariables  = require('postcss-css-variables'),
    postcssImport = require('postcss-import');

let paths = (args.paths || '').split(',');

if (!fs.existsSync(args.src)) {
    !process.exit(0);
}

let postcss_plugins = [
    postcssImport({
        path: paths,
    }),
    cssvariables(),
    colorFunction(),
];

let rollup_plugins = [
        commonjs(),
        includePaths({
            paths: paths,
        }),
        node(),
        html({
            include: '/**/*.html',
            htmlMinifierOptions: {
                collapseWhitespace: true,
                collapseBooleanAttributes: true,
            }
        }),
        postcss({
            combineStyleTags: false,
            plugins: postcss_plugins,
        }),
        json(),
];

if (args.debug) {
    rollup_plugins = rollup_plugins.concat([
    ]);
    postcss_plugins = postcss_plugins.concat([
    ]);
} else {
    rollup_plugins = rollup_plugins.concat([
    ]);
    postcss_plugins = postcss_plugins.concat([
    ]);
}

rollup.rollup({
    input: args.src,
    cache: cache,
    plugins: rollup_plugins,
}).then( function ( bundle ) {
    bundle.write({
        format: 'iife',
        file: args.dest,
    });
});

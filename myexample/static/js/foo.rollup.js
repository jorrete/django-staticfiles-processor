import Color from 'color';
import {module} from 'module.js';
import {module2} from 'myapp/js/module2.js';
import 'myapp/js/index.js';

console.log(module);
console.log(module2);
console.log(Color);
fetch('static/mydata.replace.json')
    .then(response => response.json())
    .then(console.log);

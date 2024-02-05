
// JavaScript doesn't have built-in support for DLL calls. 
// However, Node.js has a package named "ffi-napi" that provides this functionality.

// First, install the ffi-napi package using npm (Node.js Package Manager)
// npm install ffi-napi

// Then, use the following code to call the DLL function:

const ffi = require('ffi-napi');

const dll = ffi.Library('example.dll', {
  'ExampleFunction': ['int', ['int']]
});

let result = dll.ExampleFunction(5);  // Replace 5 with the actual parameter

console.log(result);

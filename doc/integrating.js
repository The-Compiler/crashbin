const request = require('request');
const CRASHBIN_URL = 'https://crashbin.example.org/api/report/new/';

process.on('uncaughtException', (err, origin) => {
    console.error(err);
    request.post(CRASHBIN_URL, {form: {title: err, log: origin}}, function() {
        process.exit(1);
    });
});

function main() {
    throw "Unhandled exception";
}

main();

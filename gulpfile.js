var gulp = require('gulp');
var rsync = require('gulp-rsync');
const path = require('path');
const files = './filesToMove.js';

var filesToMove = [
  './photobackend/*.py',
  './apps/photoapp/*.py',
    './apps/userapp/*.py',
];
function deploy(done) {
  delete require.cache[path.resolve(files)];
  gulp.src(filesToMove)
    .pipe(rsync({
      root: '',
      hostname: 'root@199.192.21.240',
      destination: '/opt/photobackend-master/',
    }))
   done();};


// The default task (called when you run `gulp` from cli) 
gulp.task('default', deploy);

{allPass, filter, inc, map} = fp = require 'fp' # auto_require:ramda

map inc, [1,2]

filter even, [1,2]

allPass even, []


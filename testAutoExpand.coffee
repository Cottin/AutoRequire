{test} = R = require 'ramda' # auto_require:ramda
{} = R = require 'ramda' # auto_require:ramda-extras
{createElement: _, DOM: {div, a}} = React = require 'react' # auto_require:react

# single line

<a><div><´`"'/{([])}/'"`´></div></a>

# multi line

...


# functions

_test = superduper (x, a, b, c) => ->
	test_123 = superduper((x, a, b, c) => ->
		test$as = (x, a, b, c) => ->
			test = () => ->
				test = (x) ->
					a = 1
					a = "'{[]}'"
		)

# functions js


{allPass, filter, inc, map, none} = R = require 'ramda' # auto_require:ramda
{createClass, createElement: _, DOM: {div, span, a}} = React = require 'react' # auto_require:react

map inc, [1,2]

filter even, [1,2]

allPass even, []




Comp = createClass
	displayName: 'name'
	mixins: [PureRenderMixin]
	render: ->
		div {},
			a {}, 'link'
			span {}, 'te'

myFunc = (a) -> a

_privateFunc = (a) -> a

func = () ->
_priv = () ->
myFunc123 = () ->
myFunc123asd = () ->
myFu_da1sd_das__da1 = () ->
MyFu_da1sd_das__da1 = () ->

MY_CONSTANT = () ->
cn = require 'classnames'

debugger

lifter = ({}, {}) ->
lifter2 = ({a, b}, {}) ->
lifter3 = ({a: {a1}, b: {b1}}, {}) ->
lifter3_1 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
lifter3_2 = ({a: {a1: {a11}, a2: {a22}, a3}, b: {b1}}, {a, b}) ->
# lifter4 = ({a: {a1, a2}, b}, {}) ->
# lifter5 = ({a: {a1: {a11}, a2}, b: {b1}}, {}) ->
# lifter6 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
# lifter7 = ({a: {a1: {a11}, a2: {a22}, a3: {a33}}, b: {b1}}, {}) ->
# lifter6 = ({a: {a1: {a111}, a2: {a222}, a3}, b: {b1}}, {}) ->




# switch between none_ and phlox below
# auto_export:phlox
module.exports = {
	lifter: {dataDeps: [], stateDeps: [], f: lifter},
	lifter2: {dataDeps: ['a', 'b'], stateDeps: [], f: lifter2},
	lifter3: {dataDeps: ['a.a1', 'b.b1'], stateDeps: [], f: lifter3},
	lifter3_1: {dataDeps: ['a.a1.a11', 'a.a2', 'a.a3.a33', 'b.b1'], stateDeps: [], f: lifter3_1},
	lifter3_2: {dataDeps: ['a.a1.a11', 'a.a2.a22', 'a.a3', 'b.b1'], stateDeps: ['a', 'b'], f: lifter3_2}
}
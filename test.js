import R, {allPass, filter, inc} from 'ramda' // auto_require:ramda
import {getPath} from 'ramda-extras' // auto_require:ramda-extras
import React, {createClass, createElement: _, DOM: {div, span, a}} from 'react' // auto_require:react

// node style
const {allPass, filter, inc} from = R = 'ramda' // auto_require:ramda

// ramda
map inc, [1,2]

filter even, [1,2]

allPass even, []

a_dec_variable = 1 // don't require
// don't require curry since this is a comment
const obj = {
	any: 1, // don't require obj keys
}

// // ramda-extras
fmap [1, 2, 3], (x) -> x + 1 - 2 / 3 * 5
getPath 'a.b.c', {}
yreduce 1, 2, 3




// # react
{createClass, createElement: _, DOM: {div, span, a}} = createClass
// 	displayName: 'name'
// 	mixins: [PureRenderMixin]
// 	render: ->
// 		div {},
// 			a {}, 'link'
// 			span {}, 'te'


// # phlox
// myFunc = (a) -> a

// _privateFunc = (a) -> a

// func = () ->
// _priv = () ->
// myFunc123 = () ->
// myFunc123asd = () ->
// myFu_da1sd_das__da1 = () ->
// MyFu_da1sd_das__da1 = () ->

// MY_CONSTANT = () ->
// cn = require 'classnames'

// debugger

// lifter = ({}, {}) ->
// lifter2 = ({a, b}, {}) ->
// lifter3 = ({a: {a1}, b: {b1}}, {}) ->
// lifter3_1 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
// lifter3_2 = ({a: {a1: {a11}, a2: {a22}, a3}, b: {b1}}, {a, b}) ->
// # lifter4 = ({a: {a1, a2}, b}, {}) ->
// # lifter5 = ({a: {a1: {a11}, a2}, b: {b1}}, {}) ->
// # lifter6 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
// # lifter7 = ({a: {a1: {a11}, a2: {a22}, a3: {a33}}, b: {b1}}, {}) ->
// # lifter6 = ({a: {a1: {a111}, a2: {a222}, a3}, b: {b1}}, {}) ->

// MySuperVM = ({a, b}, {c}) ->
// MySuperDuperVM = ({b: {b1}}, {d}) ->


// module.exports =
// 	MySuperVM: {dataDeps: ['a', 'b'], stateDeps: ['c'], f: MySuperVM} #auto_export:phlox-vm
// 	MySuperDuperVM: {dataDeps: ['b.b1'], stateDeps: ['d'], f: MySuperDuperVM} #auto_export:phlox-vm


// # switch between none_ and phlox below
// # auto_export:phlox
module.exports = {

}
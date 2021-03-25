{__, allPass, compose, cond, contains, dissoc, drop, filter, inc, innerJoin, join, map, match, max, min, none, nth, split, test, type} = R = require 'ramda' # auto_require: ramda
{change, $} = RE = require 'ramda-extras' #auto_require: ramda-extras
{createClass, createElement: _, DOM: {div, span, p, a, input}} = React = require 'react' # auto_require: react
{} = require 'negin' # auto_require: negin
[ːage, ːtest, ːcategory, ːname, ːtough_case] = ['age', 'test', 'category', 'name', 'tough_case'] #auto_sugar

# ramda
map inc, [1,2]

filter inc, [1,2]

allPass cond, []


# compose
f2 = compose inc(1), inc(2)

a_dec_variable = 1 # don't require
# don't require curry since this is a comment
msg = "CHANGE: #{join(',', dataPaths)}" # include join. Improvement: don't include innerJoin
a = dissoc(a) #
obj =
	any: 1 # don't require obj keys

# don't include keywords
allPass when, and, not, or

# ramda-extras
fmap [1, 2, 3], (x) -> x + 1 - 2 / 3 * 5
getPath 'a.b.c', {}
change.meta {a: 1}, {}, {}, {}
as Λ.dasd Λ.a
# Sugar
query =
	ـUser {gpa: {gt: 4.4}, ːname, ːage, ːtest},
		ـbff {ːname},
			ـfavoriteCourse {id: {gt: 3}, ːname}
		ـfavoriteCourse {id: 2, ːname ːcategory}

'semi_though_case:1' # shouldn't include

a = 'this is a ːtough_case ' # shouldn't include




# react
Comp = createClass
	displayName: 'name'
	mixins: [PureRenderMixin]
	render: ->
		div {},
			a {}, 'link'
			span {}, 'te'


# phlox
myFunc = (a) -> a

_privateFunc = (a) -> a

# func = () ->
# _priv = () ->
# myFunc123 = () ->
# myFunc123asd = () ->
# myFu_da1sd_das__da1 = () ->
# MyFu_da1sd_das__da1 = () ->

MY_CONSTANT = () ->
cn = require 'classnames'

debugger

# lifter = ({}, {}) ->
# lifter2 = ({a, b}, {}) ->
# lifter3 = ({a: {a1}, b: {b1}}, {}) ->
# lifter3_1 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
# lifter3_2 = ({a: {a1: {a11}, a2: {a22}, a3}, b: {b1}}, {a, b}) ->
# lifter4 = ({a: {a1, a2}, b}, {}) ->
# lifter5 = ({a: {a1: {a11}, a2}, b: {b1}}, {}) ->
# lifter6 = ({a: {a1: {a11}, a2, a3: {a33}}, b: {b1}}, {}) ->
# lifter7 = ({a: {a1: {a11}, a2: {a22}, a3: {a33}}, b: {b1}}, {}) ->
# lifter6 = ({a: {a1: {a111}, a2: {a222}, a3}, b: {b1}}, {}) ->

MySuperVM = ({a, b}, {c}) ->
MySuperDuperVM = ({b: {b1}}, {d}) ->



colors = require './colors'

warn = (msg) ->
	console.warn msg
	return {}

unit = (x, base = 0) ->
	if type(x) == 'Number'
		return (x + base) / 10 + 'rem'
	else if ! isNaN(x) # we allow numbers as strings to eg. '2' so we can be a bit lazy in parsing
		x_ = parseFloat(x)
		return (x_ + base) / 10 + 'rem'
	else
		RE = /^(-)?(\d+)\+(\d+)(vh|vw)?$/
		RE2 = /^(-?\d+)x$/
		if test RE, x
			[___, neg, num_, extra, vhvw] = match RE, x
			num = parseInt(num_) + base
			return "calc(#{neg && '-1 * ' || ''}(#{num/10}rem + #{extra * 5 / 10}#{vhvw || 'vw'}))"
		if test RE2, x # På test... känns inte som det är användbart
			[___, extra] = match RE2, x
			return parseInt(extra) * 5 / 10 + 'vh'
		else
			return x

f = (x) ->
	ret = {}
	if type(x) != 'String' then return warn "font expected type string, given: #{x}"
	
	RE = ///^
	([a-z_]) # family
	([\d]{1,2}(?:\+\d)?|_) # size
	((?:[a-z]{2,3})(?:-\d)?|__)? # color
	(\d|_)? # weight
	(\d|_)? # shadow
	$///

	if ! test RE, x then return warn "Invalid string given for font: #{x}"
	[___, family, size, clr, weight, shadow] = match RE, x

	switch weight
		when '_' then # noop
		when undefined then # noop
		else ret.fontWeight = parseInt(weight) * 100

	switch family
		# when 'a' then ret.fontFamily = "Avenir"
		# when 'a' then ret.fontFamily = "Open Sans"
		# when 'a' then ret.fontFamily = "Noto Sans"
		when 'a'
			fam = 'Avenir LT W01_'
			if weight == '3' then ily = '35 Light1475496'
			else if weight == '4' then ily = '45 Book1475508'
			else if weight == '5'
				ily = '55 Roman1475520'
				# Workaround to get font.com Roman a bit thicker, closer to installed Avenir.
				# Disabled. Only improvement for Chrome, Firefox makes it super thick.
				# ret.fontWeight = 'bold' 
			else if weight == '6' then ily = '65 Medium1475532'
			else if weight == '9' then ily = '95 Black1475556'
			else warn "Invalid weight for family Avenir: #{weight}"
			ret.fontFamily = "\"#{fam+ily}\", Avenir, Sans-Serif"
		when 'l' then ret.fontFamily = "Lato"
		when '_' then # no-op
		else return warn "invalid family '#{family}' for t: #{x}"

	if size != '_' then ret.fontSize = unit size, 0

	if clr && clr != '__' then ret.color = colors(clr)

	switch shadow
		when '1' then ret.textShadow = '1px 1px 1px rgba(90,90,90,0.50)'
		when '2' then ret.textShadow = '1px 2px 0px #893D00'
		when '3' then ret.textShadow = '1px 2px 0px #000000'
		when undefined then # no-op
		when '_' then # noop
		else return warn "invalid text shadow '#{shadow}' for t: #{x}"

	return ret

bord = (x) -> border '', x
borb = (x) -> border '-bottom', x
bort = (x) -> border '-top', x
borl = (x) -> border '-left', x
borr = (x) -> border '-right', x


border = (side, x) ->
	RE = new RegExp("^(#{colors.REstr})(_(\\d))?$")
	if ! test RE, x then return warn "Invalid string given for border: #{x}"
	[___, clr, ____, size] = match RE, x

	"border#{side}": "#{unit(size || 1)} solid #{colors(clr)}"

place = (clr) ->
	color = colors(clr)

	#https://css-tricks.com/almanac/selectors/p/placeholder/
	'::-webkit-input-placeholder': {color} # Chrome/Opera/Safari
	'::-moz-placeholder': {color} # Firefox 19+
	':-ms-input-placeholder': {color} # IE 10+
	':-moz-placeholder': {color} # Firefox 18-

fs = (x) ->
	if x == 'i' then fontStyle: 'italic'
	else warn "invalid font style '#{x}'"

ls = (x) -> letterSpacing: unit x

colorHelp = (x) ->
	devColors = ['lime', 'white', 'teal', 'pink', 'red', 'green', 'blue', 'yellow', 'lightblue']
	if contains x, devColors then return x
	else return colors x


bg = (x) -> backgroundColor: colorHelp x

fill = (x) -> fill: colorHelp x

op = (x) -> opacity: if x == 0 then 0 else x/10

ol = (x) -> outline: x

cur = (x) ->
	switch x
		when 'p' then cursor: 'pointer'
		else warn "invalid cur(sor) '#{x}'"

sh = (v) ->
	res = match /^(-?\d+)_(-?\d+)_(\d+)_(\d+)$/, v
	if ! res then return warn "Invalid string given for shadow: #{v}"
	[x, y, blur, spread] = $ res, drop(1), map (s) -> unit parseInt s

	boxShadow: "#{x} #{y} #{blur} #{spread} rgba(0,0,0,0.24)"


_sh1 = ->
	boxShadow: '0 -1px 3px 0 rgba(0,0,0,0.24)'

_sh2 = ->
	boxShadow: '0 1px 2px 0 rgba(0,0,0,0.28)'

_sh3 = ->
	boxShadow: '0 1px 13px 1px rgba(0,0,0,0.28)'

_sh4Old = ->
	boxShadow: '0 1px 3px 0 rgba(0,0,0,0.28)'

_sh4 = ->
	boxShadow: "0 1px 0 0 #{colors 'bk-2'}";

_sh5 = ->
	boxShadow: "0 1px 2px 1px #{colors 'bk-3'}";

_sh6 = ->
	boxShadow: '0 1px 3px 0 rgba(0,0,0,0.28)'

_sh7 = ->
	boxShadow: '0 1px 4px 0 rgba(0,0,0,0.48)'

_sh8 = ->
	boxShadow: '0 1px 1px 0 rgba(0,0,0,0.28)'


_sha = (s) ->
	[h, v, blur, spread, clr] = split '_', s
	boxShadow: "#{h}px #{v}px #{blur}px #{spread}px #{colors clr}"




_tsh1 = ->
	textShadow: '1px 1px 1px rgba(0, 0, 0, 0.4)'


transi = '0.1s ease-out'
_day = ->
	# transition: transi
	# '& .dayLabels':
	# 	transition: transi
	# '& .dayLabel':
	# 	transition: transi
	'& .dayCircle':
		# transition: transi
		visibility: 'hidden'

	':hover':
		# background: colors('bu-1')
		'& .dayLabels':
			background: colors 'gya-1'
		# '& .dayLabel':
		# 	color: colors 'bk-1'
		# '& .dayCircle':
		# 	visibility: 'visible'

transi2 = '0.5s ease'
__week = ->
	'& .weekTotal':
		transition: transi2
		opacity: 0
	':hover':
		'& .weekTotal':
			opacity: 1

_hideAt = (x) ->
	"@media (max-width: #{x}px)":
		display: 'none'

_showAt = (x) ->
	"@media (min-width: #{x}px)":
		display: 'none'

_bgfade = ->
	transition: 'background-color 0.1s ease-out'

_opfade = (x) ->
	transition: "opacity #{x/10}s ease-out"

_small = ->
	transform: 'scale(0.1)'

_normal = ->
	transform: 'scale(1.0)'

_rec = ->
	# transition: transi
	# '& .white':
	# 	transition: transi
	# '& .blue':
	# 	transition: 'background ' + transi
	# '& .hh':
	# 	transition: transi
	# '& .mm':
	# 	transition: transi

	':hover':
		'& .blue':
			boxShadow: '0 1px 3px 0 rgba(0,0,0,0.38)'
			# background: colors 'bu-1'
			# borderLeft: "1px solid #{colors('wh-5')}"
			# paddingLeft: unit 11
		# '& .white':
		# 	color: colors 'wh-9'
		'& .hours':
			color: colors 'bub'
		'& .minutes':
			color: colors 'bub-5'


_blur = ->
	filter: "url('#blur1')"

_lingr = ->
	background: 'linear-gradient(-180deg, #33C663 0%, #36AE51 100%)'


_hovgy = ->
	':focus':
		outline:0
	':hover':
		background: '#F8F8F8'
		# color: colors 'rea'

_save = ->
	':focus':
		outline:0
		background: 'linear-gradient(-180deg, #33C663 0%, #36AE51 100%)'
		color: colors 'wh'
	':hover':
		background: 'linear-gradient(-180deg, #33C663 0%, #36AE51 100%)'
		color: colors 'wh'

_lingn = ->
	background: 'linear-gradient(-180deg, #33C663 0%, #36AE51 100%)'

_extraRight = ->
	transform: 'translateX(100%)'

_extraLeft = ->
	transform: 'translateX(-100%)'

_ho = (bg) ->
	':hover':
		background: colors bg


# inspiration from: https://codepen.io/lbebber/pen/rawQKR
_menu = ->
	userSelect: 'none'
	'& .menuItemSel':
		transform: 'translate3d(0,0,0)'
	# '& .menuItem':
	# 	opacity: 0
	# 	# display: 'none'
	# 	# visibility: 'hidden'
	# 	transition: 'ease-out 180ms'

	':active':
		width: '250px'
		boxShadow: "-1px -20px 32px 43px #{colors 'bu'}"
		'& .menuItem':
			opacity: 1
			# display: 'flex'
			# visibility: 'visible'
		# '& .menuItem:nth-child(2)': transform: 'translate3d(-60px,0,0)'
		'& .menuItem:nth-child(2)': transform: 'translate3d(-120px,0,0)'
		'& .menuItem:nth-child(3)': transform: 'translate3d(-60px,0,0)'

	'+ .sib1':
		backgroundColor: 'red'

_menuOpen = ->
	width: '250px'
	boxShadow: "-1px -20px 32px 43px #{colors 'bu'}"
	'& .menuItem':
		opacity: 1
		# display: 'flex'
		# visibility: 'visible'
	# '& .menuItem:nth-child(2)': transform: 'translate3d(-60px,0,0)'
	'& .menuItem:nth-child(2)': transform: 'translate3d(-120px,0,0)'
	'& .menuItem:nth-child(3)': transform: 'translate3d(-60px,0,0)'



# switch between none_, none__ and phlox below
# auto_export: none__, test: 1
module.exports = {f2, msg, a, obj, query, a, Comp, myFunc, _privateFunc, MY_CONSTANT, MySuperVM, MySuperDuperVM, warn, unit, f, bord, borb, bort, borl, borr, border, place, fs, ls, colorHelp, bg, fill, op, ol, cur, sh, _sh1, _sh2, _sh3, _sh4Old, _sh4, _sh5, _sh6, _sh7, _sh8, _sha, _tsh1, transi, _day, transi2, __week, _hideAt, _showAt, _bgfade, _opfade, _small, _normal, _rec, _blur, _lingr, _hovgy, _save, _lingn, _extraRight, _extraLeft, _ho, _menu, _menuOpen, test: 1}
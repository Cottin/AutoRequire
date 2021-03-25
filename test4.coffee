{any, contains, curry, empty, isEmpty, isNil, keys, length, match, replace, test, toUpper, type} = R = require 'ramda' #auto_require: ramda
{$, sf0, satisfies} = RE = require 'ramda-extras' #auto_require: ramda-extras
[ːkeys] = ['keys'] #auto_sugar
qq = (f) -> console.log match(/return (.*);/, f.toString())[1], f()
qqq = (...args) -> console.log ...args
_ = (...xs) -> xs

require 'dayjs/locale/en-gb'
dayjs = require 'dayjs'
dayjs.locale('en-gb') # en-gb starts week on monday, en does not
quarterOfYear = require 'dayjs/plugin/quarterOfYear'
dayjs.extend quarterOfYear
weekOfYear = require 'dayjs/plugin/weekOfYear'
dayjs.extend weekOfYear

{WeirdError} = require './errors'

_YYYYMMDD = 'YYYY-MM-DD'

###### VERY EXPERIMENTAL, WATCH OUT ####################
# Crashes popsiql and gives warning in react... not worth it :)
# ramdaProxy = (o) ->
# 	return new Proxy o,
# 		get: (target, prop) ->
# 			f = R[prop]
# 			if f.length == 1 then () -> ramdaProxy f target
# 			else if f.length == 2 then (x) -> ramdaProxy f x, target
# 			else if f.length == 3 then throw new Error 'r() does not support functions with 3 arguments yet'
# 			else throw new Error ':::' + prop


# Object.prototype.r = () -> ramdaProxy @
################# NEW IDEA #############################
# https://stackoverflow.com/a/20728736

# ramdaProxy = (_o) ->
# 	if _o != Object _o then o = Object _o
# 	else o = _o

# 	return new Proxy o,
# 		get: (target, prop) ->
# 			f = R[prop]
# 			if !f then f = RE[prop]

# 			console.log prop
# 			if !f then target[prop]
# 			else if f.length == 1 then ramdaProxy f target
# 			else if f.length == 2 then (x) -> ramdaProxy f x, target
# 			else if f.length > 2 then throw new Error 'r() does not support functions with 3 arguments yet'

# ext_obj = [ːkeys]

# exts = ext_obj.concat [], []

# Object.defineProperty Object.prototype, 'r',
# 	value: () ->
# 		return ramdaProxy @

# for k in exts
# 	if Object.prototype[k] then continue
# 	Object.defineProperty Object.prototype, k,
# 		value: () ->
# 			f = R[k]
# 			if !f then f = RE[k]

# 			if f.length == 1 then () -> ramdaProxy f @
# 			else if f.length == 2 then (x) -> ramdaProxy f x, @
# 			else if f.length == 3 then throw new Error 'ramdaExt does not support functions with 3 arguments yet'
# 			else throw new Error ':::' + prop

# console.log {a: 1}.r().keys.length
# test1 = {a: 1}.r().keys.length
# console.log test1
# console.log test1.gt(1)
# if !test1.gt(1) then console.log 'Problem'
# if Boolean(false) then console.log 'Propblem x 2'
# console.log Number(1) > 2

# Object.defineProperty Object.prototype, 'reverse',
# 	value: () ->
# 		return reverse @

# console.log [1, 2, 3] .reverse()



########################################################

# Many libraries behave different based on NODE_ENV in optimization, logging etc.
# To keep environments as simialar as possible to prod we keep NODE_ENV set to production and use ENV instead.
# Local: NODE_ENV=dev ENV=dev, Test: NODE_ENV=production ENV=test, Prod: NODE_ENV=production ENV=prod
isEnvProd = () -> process.env.ENV == 'prod'
isEnvProdOrTest = () -> process.env.ENV == 'prod' || process.env.ENV == 'test'
isEnvDev = () -> process.env.ENV == 'dev'

# Proxy for date related utils
df =
	# Mo = 0, Su = 6
	dayOfWeek: (date) ->
		dow = dayjs(date).day()
		if dow == 0 then 6
		else dow - 1
	format: curry (format, _date) ->
		if type(_date) == 'Number' && _date < 9000000000 then date = 1000 * _date # epoch seconds to milliseconds
		else date = _date

		if format == 'W' then dayjs(date).week() # shorthand for simple format W and Q
		else if format == 'Q' then dayjs(date).quarter()
		else if format == 'Dth'
			dateS = dayjs(date).format 'D'
			dateI = parseInt dateS
			ordinal = switch dateI
				when 1 then 'st'
				when 2 then 'nd'
				when 3 then 'rd'
				else 'th'
			return "#{dateS}#{ordinal}"
		else dayjs(date).format(format)
	diff: curry (early, late, unit) -> dayjs(late).diff(early, unit)
	get: curry (unit, date) -> dayjs(date).get(unit)
	isAfter: (date1, date2, unit = undefined) -> dayjs(date1).isAfter(date2, unit)
	isSame: (date1, date2, unit = undefined) -> dayjs(date1).isSame(date2, unit)
	yyyymmdd: (date) -> dayjs(date).format 'YYYY-MM-DD'

	# Tid mostly handles dates and we save quite a bit of complexity by defaulting to not care about time
	add: curry (num, unit, date) -> dayjs(date).add(num, unit).format(_YYYYMMDD)
	subtract: curry (num, unit, date) -> dayjs(date).subtract(num, unit).format(_YYYYMMDD)
	startOf: curry (unit, date) -> dayjs(date).startOf(unit).format(_YYYYMMDD)
	endOf: curry (unit, date) -> dayjs(date).endOf(unit).format(_YYYYMMDD)

	t: # use df.t if you need to handle time and not only date
		add: curry (num, unit, date) -> dayjs(date).add(num, unit).format()
		subtract: curry (num, unit, date) -> dayjs(date).subtract(num, unit).format()
		startOf: curry (unit, date) -> dayjs(date).startOf(unit).format()
		endOf: curry (unit, date) -> dayjs(date).endOf(unit).format()

sleep = (ms) -> new Promise (resolve) -> setTimeout(resolve, ms)

toShortString = (x) ->
	if 'Array' == type x
		len = length x
		if len == 0 then return "[] (empty)"
		else if len == 1 then return "[ {} ] (1 item)"
		else if len == 2 then return "[ {}, {} ] (2 items)"
		else if len > 2 then return "[ {}, {}, ... ] (#{len} items)"
	else if 'Object' == type x
		return "{ id: #{x.id}, ... }"
	else
		return res

ensureSpec = (o, spec, errorMsg) ->
	res = satisfies o, spec
	if !isEmpty res then throw new Error "#{errorMsg} #{sf0 res}"

vatFor = (countryCode) ->
	eu =
		AT: 20, BE: 21, BG: 20, CY: 19, CZ: 21, DE: 19, DK: 25, EE: 20, EL: 24, ES: 21, FI: 24, FR: 20,
		HR: 25, HU: 27, IE: 23, IT: 22, LT: 21, LU: 17, LV: 21, MT: 18, NL: 21, PL: 23, PT: 23, RO: 19,
		SE: 25, SI: 22, SK: 20, UK: 20

	return eu[countryCode] || 0

isEU = (countryCode) -> vatFor(countryCode) > 0

isEurope = (countryCode) ->
	europeanOutsideEU = ['AL', 'AD', 'AM', 'BY', 'BA', 'FO', 'GE', 'GI', 'IS', 'IM', 'XK', 'LI', 'MK', 'MD',
	'MC', 'MN', 'NO', 'RU', 'SM', 'RS', 'CH', 'TR', 'UA', 'GB', 'VA']

	if vatFor(countryCode) > 0 then true
	else if contains countryCode, europeanOutsideEU then true
	else false

parseVAT = (vat) ->
	if isNil vat then return [undefined, undefined]
	return [toUpper(vat.substr(0, 2)), vat.substr(2)]

countryUsesStates = (countryCode) ->
	if !countryCode then return false
	# List from https://github.com/substack/provinces
	countriesUsingStates = ['US', 'GB', 'CA', 'MX', 'AU', 'CN', 'DE', 'BE', 'NL', 'DK', 'TR', 'ID', 'JO',
	'IN', 'KH', 'ET', 'PE', 'CU', 'AR', 'CL', 'BO', 'ES', 'BD', 'PK', 'NG', 'JP', 'AT', 'BR', 'PH', 'VN', 'CR']

	return contains countryCode, countriesUsingStates

countryStateType = (countryCode) ->
	switch countryCode
		when 'US' then 'State'
		when 'BE' then 'Province'
		else 'State, provice, region'

currencyFor = (countryCode) ->
	if countryCode == 'UK' then return 'GBP'
	if countryCode == 'SE' then return 'SEK'
	else if isEurope countryCode then return 'EUR'
	else return 'USD'

currencySymbol = (currency) ->
	switch currency
		when 'GBP' then '£'
		when 'EUR' then '€'
		when 'USD' then '$'
		when 'SEK' then 'kr'
		else '$'



# priceFor = (currency) ->
# 	switch currency
# 		when 'GBP' then 8000000
# 		when 'EUR' then 9000000
# 		when 'USD' then 9000000
# 		when 'SEK' then 90000000
# 		else 9000000

# monthlyToYearly = (monthlyPrice) -> monthlyPrice * 0.85

formatPrice = (n, removeZero = false) ->
	if removeZero && n % 100 == 0 then return '' + n/100
	return '' + (n/100).toFixed(2)

formatCurrency = (amount, currency, removeZero = false) ->
	switch currency
		when 'GBP' then "£#{formatPrice amount, removeZero}"
		when 'EUR' then "#{formatPrice amount, removeZero} €"
		when 'SEK' then "#{replace('.', ',', formatPrice(amount, removeZero))} kr"
		else "$#{formatPrice amount, removeZero}"
		# else throw new Error "NYI currency #{currency}"

_currentDeal = 'from20201001'
_deals =
	from20201001:
		test:
			month:
				USD: {priceId: 'price_1HMxiIDDW8849IySx1WgJm0m', amount: 900}
				EUR: {priceId: 'price_1HMxikDDW8849IySNCSZ4vGb', amount: 900}
				SEK: {priceId: 'price_1HACR4DDW8849IySoUIiUlUp', amount: 9000}
			year:
				USD: {priceId: 'price_1HL8waDDW8849IySoZj3eH4W', amount: 9180}
				EUR: {priceId: 'price_1HL8wuDDW8849IySITuWLYNu', amount: 9180}
				SEK: {priceId: 'price_1HL8vqDDW8849IySE16PEZQV', amount: 91800}
		prod:
			todo: 1

getPrices = (priceId) ->
	envKey = if isEnvProd() then 'prod' else 'test' # ENV=dev gives 'test' here
	if !priceId then return _deals[_currentDeal][envKey]

	pricesToSearch = null

	for deal, envs of _deals
		for interval, currencies of envs[envKey]
			for currency, priceDef of currencies
				if priceId == priceDef.priceId then return envs[envKey]

	throw new WeirdError "priceId #{priceId} does not match any existing prices"

getPriceFor = ({isYear, currency}) ->
	prices = getPrices()
	return prices[isYear && 'year' || 'month'][currency]

getPriceFor2 = ({isYear, currency}) ->
	prices = getPrices()
	return prices[isYear && 'year' || 'month'][currency]

getPrice = ({isYear, country, useVatNo, currentPriceId = null}) ->
	currency = currencyFor country
	vatPercent = vatFor country
	prices = getPrices currentPriceId
	period = if isYear then 'year' else 'month'
	if isYear then pricePerMonth = prices.year[currency].amount / 12
	else pricePerMonth = prices.month[currency].amount
	pricePerMonthF = formatCurrency pricePerMonth, currency
	subtotal = if isYear then pricePerMonth * 12 else pricePerMonth
	subtotalF = formatCurrency subtotal, currency
	vat = subtotal * vatPercent / 100
	vatF = formatCurrency vat, currency
	if useVatNo
		vat = 0
		vatPercent = 0
	total = subtotal + vat
	totalF = formatCurrency subtotal, currency

	return {total, totalF, subtotal, subtotalF, vatPercent, vat, vatF, period, pricePerMonth, pricePerMonthF}


#auto_export: none_
module.exports = {isEnvProd, isEnvProdOrTest, isEnvDev, df, sleep, toShortString, ensureSpec, vatFor, isEU, isEurope, parseVAT, countryUsesStates, countryStateType, currencyFor, currencySymbol, formatPrice, formatCurrency, getPrices, getPriceFor, getPriceFor2, getPrice}
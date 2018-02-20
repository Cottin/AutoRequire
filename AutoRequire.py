import sublime
import sublime_plugin
import re
import json
import platform
import os
import os.path as path

# fp helpers
def contains(x):
	def f(xs):
		return (x in xs)
	return f

def doesNotContain(x):
	def f(xs):
		return not (x in xs)
	return f

def isTruthy(x):
	return not not x

def trim(s):
	return s.strip()

# from stack overflow
def flatten(l, a):
  for i in l:
      if isinstance(i, list):
          flatten(i, a)
      else:
          a.append(i)
  return a


class AutoRequire(sublime_plugin.TextCommand):
	def run(self, edit, user_input=None):

		global_settings = sublime.load_settings(self.__class__.__name__+'.sublime-settings')
		auto_requires = self.view.settings().get('auto_require', global_settings.get('auto_require', '.*'))

		isJs = re.search(r'\.js$', self.view.file_name()) is not None

		# find keeps returning (-1, -1) instead of None, so added a safety here :)
		safety = 0

		startPos = 0
		while True:
			safety = safety + 1
			if safety > 100:
				break

			region = self.view.find(".*auto_require", startPos)

			if region is None:
				break

			# find keeps returning (-1, -1) instead of None, don't know why
			if region.a < 0 or region.b < 0:
				break


			line = self.view.line(region)	
			line_text = self.view.substr(line)
			name_search = re.search("auto_require:(.*)", line_text)
			if name_search is None:
				return
			name = name_search.group(1)


			require_to_use = None

			for r in auto_requires:
				if name == r['name']:
					require_to_use = r
					break

			if require_to_use is None:
				return

			keywords_to_use = []
			nested_keywords = {}
			for k in require_to_use["keywords"]:
				if k in keywords_to_use: continue

				if isinstance(k, dict):
					if "group" in k:
						nested = []
						for k_ in k["keywords"]:
							if self.view.find("[^a-zA-Z\@\.]" + k_ + "[^a-zA-Z]", region.b):
								nested.append(k_)

						nested_keywords[k["group"]] = nested
					if "aliasFor" in k:
						keywords_to_use.append(k['aliasFor'] + ": " + k['name'])

				else:
					regKs = self.view.find_all("[^a-zA-Z\@\._]" + k + "[^a-zA-Z\@\._\:]")
					for regK in regKs:
						lineWithK = self.view.line(regK.a)
						if re.search(r'auto_require', self.view.substr(lineWithK)):
							continue

						strToK = self.view.substr(sublime.Region(lineWithK.a, regK.b))
						if isJs:
							if re.search(r'\/\/', strToK): continue
						else:
							hashMatch = re.search(r'#', strToK)
							if hashMatch:
								charAfterHash = strToK[hashMatch.span()[1] : hashMatch.span()[1]+1]
								if charAfterHash is not '{': continue

						keywords_to_use.append(k)
						break # we only add it once

			# note: the ? is needed for un-greedy match so that {} = R = require 'ramda' is replaced with
			#				{map, filter} = R ... instead of {map, filter} = require 'ramda'

			topLevels = ", ".join(keywords_to_use)

			nested = ""
			for g in nested_keywords:
				if len(nested_keywords[g]) > 0:
					nested += g + ": {" + ", ".join(nested_keywords[g]) + "}"

			items = list(filter(isTruthy, [topLevels, nested]))

			replacement_region = self.view.find("\{.*\}", region.a)
			result = "{" + ", ".join(items) + "}"

			self.view.replace(edit, replacement_region, result)

			line = self.view.line(region.a)
			startPos = line.b



# Reference implementation in CoffeeScript below.
# Use the coffee in a BrowserRepl to work with and when finished,
# translate the code to python... much easier.
# ------------------------------------------
# console.clear()
# parse = (s, path=[]) ->
# 	console.log 'parse', s, path
# 	s_ = replace /\s/g, '', s
# 	s__ = cc drop(1), dropLast(1), s_
# 	items = []
# 	nested = {}
# 	count = 0
# 	word = ''
# 	nest = ''
# 	for c in s__
# 		if count > 0
# 			nest += c
# 			if c == '{' then count++
# 			else if c == '}'
# 				count--
# 				if count == 0
# 					nested[word] = nest
# 					nest = ''
# 					word = ''
# 		else
# 			if test /[a-zA-Z0-9_$]/, c
# 				word += c
# 			else if c == ',' && word != ''
# 				items.push(cc join('.'), append(word), path)
# 				word = ''
# 			else if c == ':' then # noop
# 			else if c == '{'
# 				count++
# 				nest += c
# 	if word != ''
# 		items.push(cc join('.'), append(word), path)
# 	subParse = ([k, v]) -> parse v, append(k, path)
# 	nested_ = cc flatten, map(subParse), toPairs, nested
# 	return cc sortBy(identity), concat(items), nested_
# # parse '{a,    b}'
# # parse '{a: {a1}, b: {b1, b2}, c}'
# # parse '{a: {a1: {a11}, a2, a3: {a33}}, b}'
# # parse '{a: {a1: {a11}, a2: {a22}, a3}, b: {b1}}'
# --------------------------------------
def parse(s, path=[]):
	# print('parse', s, path)
	s_ = re.sub(r'\s', '', s)
	s__ = s_[1:-1]
	items = []
	nested = {}
	count = 0
	word = ''
	nest = ''
	for c in s__:
		if count > 0:
			nest += c
			if c == '{': count += 1
			elif c == '}':
				count -= 1
				if count == 0:
					nested[word] = nest
					nest = ''
					word = ''
		else:
			if re.match(r'[a-zA-Z0-9_$]', c):
				word += c
			elif c == ',' and word != '':
				items.append('.'.join(path + [word]))
				word = ''
			# elif c == ':': # noop
			elif c == '{':
				count += 1
				nest += c
	if word != '':
		items.append('.'.join(path + [word]))

	nested_ = []
	def subParse(k, v):
		return parse(v, path+[k])
	for k in nested:
		nested_.append(subParse(k, nested[k]))
	nested__ = flatten(nested_, [])
	return sorted(items + nested__)


class AutoExport(sublime_plugin.TextCommand):
	def run(self, edit, user_input=None):

		print('auto_export! -----------------------------')
		top_regions = self.view.find_all("auto_export")

		for region in top_regions:
			export_line = self.view.line(region)	
			export_line_text = self.view.substr(export_line)
			search = re.search("auto_export:(.*)", export_line_text)
			if search is None:
				return
			name = search.group(1)
			# print('name', name)

			if name == 'none_':
				exports = []

				regions = self.view.find_all("^([a-zA-Z]+[a-zA-Z_0-9]*) =(.*)")

				for r in regions:
					line = self.view.line(r)	
					line_text = self.view.substr(line)
					search = re.search("^([a-zA-Z]+[a-zA-Z_0-9]*) =(.*)", line_text)
					if search is None:
						continue
					left = search.group(1)
					right = search.group(2)
					if contains('require')(right):
						continue

					exports.append(left)

				replacement_region = sublime.Region(export_line.b + 1, 9999)
				exportStr = "module.exports = {" + ", ".join(exports) + "}"
				self.view.replace(edit, replacement_region, exportStr)

			elif name == 'phlox':
				# print('phlox')
				exports = []

				regions = self.view.find_all("^([a-zA-Z$]+[a-zA-Z$_0-9]+) = \({(.*)}, {(.*)}\)")

				for r in regions:
					line = self.view.line(r)	
					line_text = self.view.substr(line)
					search = re.search("^([a-zA-Z$]+[a-zA-Z$_0-9]+) = \((\{.*\}), (\{.*\})\)", line_text)
					if search is None:
						continue
					name = search.group(1)
					data = search.group(2)
					state = search.group(3)
					def appendTics(st):
						return "'" + st + "'"

					data_ = parse(data)
					data__ = list(map(appendTics, data_))
					state_ = parse(state)
					state__ = list(map(appendTics, state_))

					exStr =  '\t' + name + ': {dataDeps: [' + ', '.join(data__) + '], stateDeps: [' + ', '.join(state__) + '], f: ' + name + '}'
					exports.append(exStr)

				replacement_region = sublime.Region(export_line.b + 1, 9999)
				exportStr = "module.exports = {\n" + ",\n".join(exports) + "\n}"
				self.view.replace(edit, replacement_region, exportStr)
			elif name == 'phlox-vm':
				# print('phlox-vm')
				exports = []

				search = re.search("([a-zA-Z$]+[a-zA-Z$_0-9]+): ", export_line_text)
				VM_name = search.group(1)

				regions = self.view.find_all("^"+VM_name+" = \({(.*)}, {(.*)}\)")

				for r in regions:
					line = self.view.line(r)	
					line_text = self.view.substr(line)
					search = re.search("^([a-zA-Z$]+[a-zA-Z$_0-9]+) = \((\{.*\}), (\{.*\})\)", line_text)
					if search is None:
						continue
					name = search.group(1)
					data = search.group(2)
					state = search.group(3)

					def appendTics(st):
						return "'" + st + "'"

					data_ = parse(data)
					data__ = list(map(appendTics, data_))
					state_ = parse(state)
					state__ = list(map(appendTics, state_))

					exStr =  '\t' + name + ': {dataDeps: [' + ', '.join(data__) + '], stateDeps: [' + ', '.join(state__) + '], f: ' + name + '}'

					self.view.replace(edit, export_line, exStr + ' #auto_export:phlox-vm')




		

# inspiration stolen from https://github.com/alexnj/SublimeOnSaveBuild/blob/master/SublimeOnSaveBuild.py
class AutoRequireEventListener(sublime_plugin.EventListener):
		def on_pre_save(self, view):
			view.run_command("auto_require")
			view.run_command("auto_export")


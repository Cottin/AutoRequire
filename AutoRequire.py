import sublime
import sublime_plugin
import re
import json
import platform
import os
import os.path as path
import codecs

import sys
import time
import subprocess 
from subprocess import Popen, PIPE

import urllib 
from urllib import request, parse
from urllib.error import HTTPError

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

		now_region = self.view.find('\d+#now_no'+'w_now', 0)
		self.view.replace(edit, now_region, str(round(time.time()*1000)) + '#now_n'+'ow_now')

		global_settings = sublime.load_settings(self.__class__.__name__+'.sublime-settings')
		auto_requires = self.view.settings().get('auto_require', global_settings.get('auto_require', '.*'))

		isJs = re.search(r'\.js$', self.view.file_name()) is not None

		if re.search(r'\.js$|\.coffee', self.view.file_name()) is None:
			return

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
			name_search = re.search("auto_require: (.*)", line_text)
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
			print(123455)
			print(require_to_use)
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
					# if k.startswith("REGEX:"):
					# 	print('regex!')
					print(name)

					regKs = []
					isRegEx = k.startswith('===')
					if isRegEx:
						regKs = self.view.find_all("[^a-zA-Z\@\._]" + r""+k[3:] + "[^a-zA-Z\@_\:]")
					else:
						regKs = self.view.find_all("[^a-zA-Z\@\._]" + re.escape(k) + "[^a-zA-Z\@_\:]")
					for regK in regKs:
						lineWithK = self.view.line(regK.a)
						if re.search(r'auto_require', self.view.substr(lineWithK)):
							continue

						strToK = self.view.substr(sublime.Region(lineWithK.a, regK.b))
						regKstr = self.view.substr(sublime.Region(regK.a + 1, regK.b - 1))
						if isJs:
							if re.search(r'\/\/', strToK): continue
						else:
							hashMatch = re.search(r'#', strToK)
							if hashMatch:
								charAfterHash = strToK[hashMatch.span()[1] : hashMatch.span()[1]+1]
								if charAfterHash is not '{': continue

						if isRegEx:
							if regKstr not in keywords_to_use:
								keywords_to_use.append(regKstr)
						else:
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

			if name == 'esramda':
				replacement_region = self.view.find(".*?(#|\/\/)", region.a)
				def wrapes(s):
					return 'import ' + s + ' from "ramda/es/' + s + '";'
				comment = '//' if isJs else '#'
				result = ' '.join(list(map(wrapes, keywords_to_use))) + ' ' + comment
				self.view.replace(edit, replacement_region, result)
			elif name == 'srcramda':
				replacement_region = self.view.find(".*?#", region.a)
				def wrapes(s):
					return s + " = require('ramda/src/" + s + "');"
				result = ' '.join(list(map(wrapes, keywords_to_use))) + ' #'
				self.view.replace(edit, replacement_region, result)
			if name == 'esramda-extras':
				replacement_region = self.view.find(".*?(#|\/\/)", region.a)
				comment = '//' if isJs else '#'
				result = 'import {' + ', '.join(keywords_to_use) + '} from "ramda-extras" ' + comment
				self.view.replace(edit, replacement_region, result)
			else:
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
# # parse '{a,	b}'
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
		print(top_regions)

		for region in top_regions:
			export_line = self.view.line(region)	
			export_line_text = self.view.substr(export_line)
			print('export_line_text', export_line_text)
			search = re.search("auto_export: (.*)", export_line_text)
			print('search', search)
			if search is None:
				return
			name = search.group(1)
			print('name', name)

			if name.startswith('none__'):
				none_search = re.search("^none__(.*)", name)
				extra = none_search.group(1)
				extraStr = ''
				if extra:
					extraStr = extra

				exports = []

				regions = self.view.find_all("^([_a-zA-Z]+[a-zA-Z_0-9]*) =(.*)")

				for r in regions:
					line = self.view.line(r)	
					line_text = self.view.substr(line)
					search = re.search("^([_a-zA-Z]+[a-zA-Z_0-9]*) =(.*)", line_text)
					if search is None:
						continue
					left = search.group(1)
					right = search.group(2)
					if contains('require')(right):
						continue

					exports.append(left)

				replacement_region = sublime.Region(export_line.b + 1, 99999999)

				print(replacement_region)
				exportStr = "module.exports = {" + ", ".join(exports) + extraStr + "}"
				self.view.replace(edit, replacement_region, exportStr)

			elif name.startswith('none_'):
				none_search = re.search("^none_(.*)", name)
				extra = none_search.group(1)
				extraStr = ''
				if extra:
					extraStr = extra

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
					if left == 'qq' or left == 'qqq':
						continue

					exports.append(left)

				replacement_region = sublime.Region(export_line.b + 1, 9999)
				exportStr = "module.exports = {" + ", ".join(exports) + extraStr + "}"
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

					exStr =	'\t' + name + ': {dataDeps: [' + ', '.join(data__) + '], stateDeps: [' + ', '.join(state__) + '], f: ' + name + '}'
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

					exStr =	'\t' + name + ': {dataDeps: [' + ', '.join(data__) + '], stateDeps: [' + ', '.join(state__) + '], f: ' + name + '}'

					self.view.replace(edit, export_line, exStr + ' #auto_export:phlox-vm')


class AutoSugar(sublime_plugin.TextCommand):
	def run(self, edit, user_input=None):

		sugar_regions = self.view.find_all("auto_sugar")
		if not sugar_regions: return

		if not re.search(r'\.coffee$', self.view.file_name()): return

		line = self.view.line(sugar_regions[0])
		# if we leave this, we'll get matches here
		self.view.replace(edit, line, "auto_sugar_temp_replacement")

		print('auto_sugar! ---------------------------------')

		# regions1 = self.view.find_all("\s(:\w+)")
		regions1 = self.view.find_all("[\[\(\s\{](:\w+)")

		for r in regions1:
			s = self.view.substr(r)
			self.view.replace(edit, r, s.replace(':', 'ː'))

		regions2 = self.view.find_all("(ː\w+)")

		xs = []
		for r in regions2:
			s = self.view.substr(r)
			xs.append(s)

		uniqueXs = list(set(xs))

		line = self.view.line(self.view.find_all("auto_sugar_temp_replacement")[0])
		line_text = self.view.substr(line)
		left = "[" + ", ".join(uniqueXs) + "]"
		right = "[" + ", ".join(["'" + x.replace("ː", "") + "'" for x in uniqueXs]) + "]"
		sugar = left + " = " + right
		self.view.replace(edit, line, sugar + " #auto_sugar")


class AutoRequireSetup(sublime_plugin.TextCommand):
	def run(self, edit, user_input=None):
		if not re.search(r'\.coffee$', self.view.file_name()): return

		regions = self.view.find_all("auto_require: ?ramda|auto_require: ?ramda-extras|auto_sugar|qqq? = \(f\)")
		for region in reversed(regions):
			line = self.view.full_line(region)
			self.view.erase(edit, line)


		self.view.insert(edit, self.view.text_point(0, 0), "{} = R = require 'ramda' #auto_require: ramda\n\
{} = RE = require 'ramda-extras' #auto_require: ramda-extras\n\
[] = [] #auto_sugar\n\
qq = (f) -> console.log match(/return (.*);/, f.toString())[1], f()\n\
qqq = (f) -> console.log match(/return (.*);/, f.toString())[1], JSON.stringify(f(), null, 2)\n\
_ = (...xs) -> xs\n\
")

		self.view.run_command("save")


######### POPSIQL

def extractBlock(self):
	for region in self.view.sel():

		# Only interested in empty regions, otherwise they may span multiple	
		# lines, which doesn't make sense for this command.	
		if not region.empty():
			return

		# Expand the region to the full line it resides on, excluding the newline	
		line = self.view.line(region)	

		cur_pt = region.b

		self.view.find
		start = 0
		end = self.view.size()

		next_newline = self.view.find("\n\s*\n", cur_pt)
		if next_newline.a != -1:
			end = next_newline.a

		# couldn't find "find previous" command
		all_newlines = self.view.find_all("\n[\s]*\n")
		for rg in all_newlines:
			if rg.b <= cur_pt:
				start = rg.b

		newRegion = sublime.Region(start, end)

		return self.view.substr(newRegion)

def runPopen(args):
	proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	com_result = proc.communicate()
	if com_result[1] != b'':
		raise Exception('runPopen ' + ' '.join(args) + ' gave error:' + str(com_result[1], 'utf-8'))
	return str(com_result[0], "utf-8")
	# alternative ways of executing things:
	# os.system('echo "' + result + '" >> temp_file.js')
	# print(os.popen('js2coffee temp_file.js').read())

popsiql_endpoint = None
class AutoRequireChooseEndpoint(sublime_plugin.TextCommand):
	def run(self, edit):
		global_settings = sublime.load_settings('Popsiql.sublime-settings')
		popsiql_settings = self.view.settings().get('popsiql', global_settings.get('popsiql', '.*'))
		self.endpoints = popsiql_settings['endpoints']
		self.view.window().show_quick_panel(self.endpoints, self.on_done)


	def on_done(self, index):

		# if canceled (esc key), index is returned as -1
		if index == -1:
			return

		print('..........')
		print(self.endpoints[index])
		global popsiql_endpoint
		popsiql_endpoint = self.endpoints[index]

class AutoRequireGotoSomething(sublime_plugin.TextCommand):
	def run(self, edit):
		print('! GOTO something ---------------------------------')
		something_defs = []
		defs_regions = self.view.find_all(r'goto_something:(.*)', 0, '$1', something_defs)
		patterns = something_defs[0].split('///')
		if len(patterns) == 0:
			patterns = ['^(\w*) ='] # default if nothing else specified
		somethings = []
		for p in patterns:
			extractions = []
			something_regions = self.view.find_all(p, 0, '$1', extractions)
			for [ex, reg] in zip(extractions, something_regions):
				if len(ex) > 0 and reg.a > defs_regions[0].b:
					somethings.append([ex, reg])
		somethings.sort(key=lambda x: x[1].a)
		texts = [x[0] for x in somethings]
		self.somethings = somethings
		self.view.window().show_quick_panel(texts, self.on_done)


	def on_done(self, index):
		# if canceled (esc key), index is returned as -1
		if index == -1:
			return

		self.view.show_at_center(self.somethings[index][1])
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(self.somethings[index][1].a, self.somethings[index][1].a))

class AutoRequireBlockCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().run_command('auto_sugar')

		global popsiql_endpoint
		if not popsiql_endpoint:
			self.view.window().run_command('auto_require_choose_endpoint')
			return


		block = extractBlock(self)
		block2 = re.sub("ː", ":", block)
		block3 = re.sub(":(\w+)", r"'ː\1': '\1'", block2)
		wrapped_code = "_ = (xs...) -> xs\nconsole.log(JSON.stringify({" + block3 + "}, (k, v) -> if v == undefined then null else v))"
		# wrapped_code = "_ = (xs...) -> xs\nconsole.log(JSON.stringify(" + block3 + "))"
		# print(wrapped_code)
		code_json = runPopen(["coffee", "-e", wrapped_code])

		url = popsiql_endpoint

		# I didn't find a way to use the lib requests which seems popular without dragging
		# it in file by file, so using urllib instead. 
		data = code_json.encode('utf-8') # data should be bytes
		headers = {'Content-Type': 'application/json'}
		req = urllib.request.Request(url, data, headers)

		did_error = False
		result_content = None
		try:
			resp = request.urlopen(req)
			result = resp.read().decode('utf-8')
			print(result)
			if result == '': result = 'null'
			wrapped_js = "console.log('var __RESULT__ = ' + require('util').inspect(" + result + ", {showHidden: false, depth: null}))"
			result_inspect = runPopen(["coffee", '-e', wrapped_js])

			# Note: important to do it right!
			# With this, the continuation doesn't work: https://www.w3schools.com/python/python_file_write.asp
			# But with this it does: https://stackoverflow.com/questions/6159900/correct-way-to-write-line-to-file
			temp_file = '/tmp/temp_file.js' 
			print(result_inspect)
			with codecs.open(temp_file, 'w', 'utf-8') as the_file:
				the_file.write(result_inspect)

			# Could maybe use Process Substitution to not have to write to file:
			# https://superuser.com/questions/939746/pass-text-to-program-expecting-a-file
			# This works in terminal: js2coffee <(echo "[{a: 1}]")  but not using subprocess.Popen
			# so using temp_file.js for now
			# proc = subprocess.Popen(["js2coffee", temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			# com_result = proc.communicate()
			# coffee_result = str(com_result[0], 'utf8')
			coffee_result_ = runPopen(["js2coffee", temp_file])
			coffee_result = re.sub("__RESULT__ = ", "", coffee_result_)
			result_content = coffee_result
			os.remove(temp_file)

		except HTTPError as err:
			result_content = err.read().decode('utf-8')
			did_error = True

		syntax_file = self.view.settings().get('syntax')

		num_groups = self.view.window().num_groups()
		active_group = self.view.window().active_group()
		# If we don't have a split view, create one and result will automatically be put on the right
		if num_groups == 1:
			self.view.window().run_command('set_layout',{
				"cols": [0.0, 0.5, 1.0],
				"rows": [0.0, 1.0],
				"cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
			})

		new_view = self.view.window().new_file()
		new_view.set_name("Result")
		point = new_view.sel()[0].begin()
		new_view.insert(edit, point, result_content)

		if did_error:
			new_view.settings().set('word_wrap', True)
		else:
			new_view.set_syntax_file(syntax_file)

		# If we already had a split view, put the result on the opposite side of the current file
		if num_groups == 2:
			move_to = 1 if active_group == 0 else 0
			self.view.window().run_command('move_to_group', {"group": move_to})









		

# inspiration stolen from https://github.com/alexnj/SublimeOnSaveBuild/blob/master/SublimeOnSaveBuild.py
class AutoRequireEventListener(sublime_plugin.EventListener):
		def on_pre_save(self, view):
			view.run_command("auto_require")
			view.run_command("auto_export")
			view.run_command("auto_sugar")


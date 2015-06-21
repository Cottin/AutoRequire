import sublime
import sublime_plugin
import re
import json
import platform
import os
import os.path as path

class AutoRequire(sublime_plugin.TextCommand):
	def run(self, edit, user_input=None):
		global_settings = sublime.load_settings(self.__class__.__name__+'.sublime-settings')

		auto_requires = self.view.settings().get('auto_require', global_settings.get('auto_require', '.*'))

		auto_require_statement_region = self.view.find(".*=.*auto_require", 0)
		line = self.view.line(auto_require_statement_region)	
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
		for k in require_to_use["keywords"]:
			if self.view.find("[^a-zA-Z\@\.]" + k + "[^a-zA-Z]", auto_require_statement_region.b):
				keywords_to_use.append(k)

		# note: the ? is needed for un-greedy match so that {} = R = require 'ramda' is replaced with
		#				{map, filter} = R ... instead of {map, filter} = require 'ramda'
		replacement_region = self.view.find(".*?=", auto_require_statement_region.a)
		self.view.replace(edit, replacement_region, "{" + ", ".join(keywords_to_use) + "} =")
		

# inspiration stolen from https://github.com/alexnj/SublimeOnSaveBuild/blob/master/SublimeOnSaveBuild.py
class AutoRequireEventListener(sublime_plugin.EventListener):
		def on_pre_save(self, view):
			view.run_command("auto_require")


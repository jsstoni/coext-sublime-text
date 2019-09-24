import sublime, sublime_plugin, os
import sys
import html.parser

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

class coextCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.code = self.getCode()
		m = re.search('(?=kudee:)\w.*', self.code)
		if m:
			ids = m.group(0)
			grupo = 'kudee:'
			urls = ids.replace(grupo, '')
			with urllib.request.urlopen(urls) as url:
				data = url.read()
				data = data.decode("utf8")
			query = "%s" %(ids)
			queryRegions = self.view.find_all ( query, sublime.LITERAL ) # literal flag is used to disable regex
			for region in reversed ( queryRegions ): # use reverse region order to avoid displacing regions with previous replacements
				self.view.replace ( edit, region, data )
	def getCode(self):
		sep = '\n\n# ' + '='*77 + '\n\n'
		code = sep.join( [self.view.substr(selection) for selection in self.view.sel() if not selection.empty()] )
		if not code:
			code = self.view.substr(sublime.Region(0, self.view.size()))
		return code
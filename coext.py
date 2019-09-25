import sublime, sublime_plugin, os, re
import sys
import html.parser

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

class coextCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.code = self.getCode()
		reg_path = '(?:\[+[0-9, ]+\]github:)'
		path = re.search('(?:\[+[0-9, ]+\])?(?=github:)\w.*', self.code)
		if path:
			ids = path.group(0)
			grupo = 'github:'
			frag = re.search(reg_path, self.code)

			if frag:
				urls = re.sub(reg_path, '', ids)
			else:
				urls = ids.replace(grupo, '')

			with urlopen(urls) as url:
				data = url.read()
				data = data.decode("utf8")
			rl = data.split('\n')
			lines = re.search('(?:\[+[0-9, ]+\])', ids)
			if lines:
				ln = lines.group(0)
				ln = re.sub('(\[|\])', '', ln)
				ln = ln.split(',')
				data = rl[int(ln[0]) : int(ln[1])]
				data = '\n'.join(data)
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
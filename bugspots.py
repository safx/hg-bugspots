#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from mercurial import ui, hg, scmutil
import datetime
import time
import math
import re


def bugspots(ui, repo, *pats, **opts):
    """Show score of bug prediction."""
    def get_fixes():
        rev = repo['tip'].rev()
        depth = opts['depth']

        restr = opts['regex'] if opts['regex'] else '|'.join(opts['words'].split(','))
        fixes = [repo[i] for i in range(rev, max(0,rev - depth), -1) if repo[i].branch() == opts['branch'] and re.search(restr, repo[i].description(), re.IGNORECASE)]
        return fixes

    def get_hotspots(fixes):
        if len(fixes) == 0: return {}
        times = sorted([i.date()[0] for i in fixes])
        now = time.mktime(datetime.datetime.now().timetuple())
        min_date = times[0]

        hotspots = {}
        for ctx in fixes:
            t = (ctx.date()[0] - min_date) / (now - min_date)
            score = 1 / (1 + math.exp(-12 * t + 12))
            for fn in ctx.files():
                if not fn in hotspots: hotspots[fn] = 0
                hotspots[fn] += score
        return hotspots

    def print_results(fixes, hotspots):
        print "Found %d bugfix commits, with %d hotspots:" % (len(fixes), len(hotspots))
        print "Fixes:"
        for i in fixes:
            t = datetime.datetime.utcfromtimestamp(i.date()[0]).ctime() if opts['display_timestamps'] else ""
            print "\t-%s #%d %s" % (t, i.rev(), i.description().split('\n')[0])

        print "Hotspots:"
        for i in sorted(hotspots, reverse=True, cmp=lambda a,b:cmp(hotspots[a],hotspots[b])):
            print "\t%.4f - %s" % (hotspots[i], i)

    fixes = get_fixes()
    hotspots = get_hotspots(fixes)
    print_results(fixes, hotspots)

 
if __name__ == '__main__':
    ui   = ui.ui()
    repo = hg.repository(ui, ".")
    predict_bug(ui, repo)


cmdtable = {
    "bugspots": (bugspots,
                 [
                  ('b', 'branch', 'default', 'branch to crawl'),
                  ('d', 'depth', 500, 'depth of log crawl') ,
                  ('r', 'regex', 'fix(es|ed)?|close(s|d)?', 'bugfix indicator regex, ie: "fix(es|ed)?" or "/fixes #(\d+)/i"'),
                  ('w', 'words', '', 'bugfix indicator word list, ie: "fixes,closed"'),
                  ('', 'display-timestamps', None, 'show timestamps of each identified fix commit')],
                 "hg bugspots [options] [FILE]")
}

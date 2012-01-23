#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from mercurial import ui, hg, scmutil
import math


def get_prediction_score(fctx):
    def get_time_list(fctx):
        return [fctx.filectx(i).changectx().date() for i in range(fctx.filerev())]

    ls = sorted(get_time_list(fctx))
    if len(ls) <= 1: return 0

    # FIXME: timezone is ignored
    min_date = ls[0][0]
    max_date = ls[-1][0]
    score = 0
    for i in ls:
        t = (i[0] - min_date) / (max_date - min_date)
        score += 1 / (1 + math.exp(-12 * t + 12))
    return score


def predict_bug(ui, repo, *pats, **opts):
    """show score of bug prediction.
       please see the details at:
       http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html
    """
    ctx = repo['tip']
    matchfn = scmutil.match(ctx, pats, opts)
    for p in matchfn:
        score = get_prediction_score(ctx[p])
        print "%.2f %s" % (score, p)

 
if __name__ == '__main__':
    ui   = ui.ui()
    repo = hg.repository(ui, ".")
    predict_bug(ui, repo)


cmdtable = {
    "predict": (predict_bug, [], "[FILE]")
}

## Mercurial Extension for Bug Prediction

This extension uses the article ``[Bug Prediction at Google | Google Engineering Tools](http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html)''.

### Install and Usage

1. Add your .hgrc:<pre>
    [extensions]
    bugprediction=/path/to/predictbug.py
</pre>
2. Type the following code in mercurial repository.<pre>
    &gt; hg predict *.cxx | sort -n
</pre>

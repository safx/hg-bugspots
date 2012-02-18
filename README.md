## Mercurial Extension for Bugspots

This extension is a port of [bugspots of git](https://github.com/igrigorik/bugspots).

### Install and Usage

1. Add your .hgrc:

        [extensions]
        bugspots=/path/to/bugspots.py

2. Just type the following code at mercurial repository.

        &gt; hg bugspots

### Usage

        hg bugspots [options] [FILE]
        
        Show score of bug prediction.
        
        options:
        
         -b --branch VALUE        branch to crawl (default: default)
         -d --depth VALUE         depth of log crawl (default: 500)
         -r --regex VALUE         bugfix indicator regex, ie: "fix(es|ed)?" or "/fixes #(\d+)/i"
                                  (default: fix(es|ed)?|close(s|d)?)
         -w --words VALUE         bugfix indicator word list, ie: "fixes,closed"
            --display-timestamps  show timestamps of each identified fix commit


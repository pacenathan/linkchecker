A fork of https://github.com/linkchecker/linkchecker that includes:

* All the [AnchorCheck fixes and improvements](https://github.com/linkchecker/linkchecker/pull/648)
    * Just add `[AnchorCheck]` to your `linkchecker.rc` to get high-performance anchor checking.
    * You might want to tune [`anchorcachesize`](https://github.com/pacenathan/linkchecker/blob/master/linkcheck/data/linkcheckerrc#L180) (in the `[checking]` section) if you see high memory use.
* The [HTTP performance fix](https://github.com/linkchecker/linkchecker/pull/658)
    * The `maxrequestspersecond` setting is now actually obeyed. If you are testing against an internal (development) web server, I suggest setting it to `1000` to get nearly the performance of checking HTML files on disk. If you are testing against public / production web servers, `10` might still be a polite value.
* A [feature to report all references to a URL](https://github.com/linkchecker/linkchecker/pull/663) (i.e. to report ALL broken links, not just the first one encountered for each target)
    * `linkchecker.rc` setting: `reportallreferences` in the `[output]` section.
    * Command line argument: `--allrefs`.
* A [fix for working with a newer (4.10+) install of BeautifulSoup](https://github.com/pacenathan/linkchecker/commit/136104ce62af0476f93e4acfb97d6cdffb8bfb01)
* A [warning when using AnchorCheck with links that point to a directory and have an anchor](https://github.com/linkchecker/linkchecker/issues/678#issuecomment-1282526281), indicating that those anchors won't be checked.

## To install

1. Clone this repository.

2. `cd path/to/this/repo`

3. `pip3 install -e .`

Now you should be able to run `linkchecker` (and do everything else, as usual) per [the main-repo docs](https://linkchecker.github.io/linkchecker/), plus the notes above.

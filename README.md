A fork of https://github.com/linkchecker/linkchecker that includes:

* All the [AnchorCheck fixes and improvements](https://github.com/linkchecker/linkchecker/pull/648)
* The [HTTP performance fix](https://github.com/linkchecker/linkchecker/pull/658)
* A [feature to report all references to a URL](https://github.com/linkchecker/linkchecker/pull/663) (i.e. to report ALL broken links, not just the first one encountered for each target)
* A [fix for working with a newer (4.10+) install of BeautifulSoup](https://github.com/pacenathan/linkchecker/commit/136104ce62af0476f93e4acfb97d6cdffb8bfb01)

## To install

1. Clone this repository.

2. `cd path/to/this/repo`

3. `pip3 install -e .`

(I'm pretty sure that will install all the python dependencies.)

Now you should be able to run `linkchecker` (and do everything else, as usual) per [the main-repo docs](https://linkchecker.github.io/linkchecker/) (which are missing the updates from this fork).

---
title: Developer Guide
layout: docs
---

### Making your first patch

1. Make sure you've signed the CLA

1. Clone the repo

   ```shell
   git clone http://github.com/tableau/document-api-python
   ```

1. Run the tests to make sure everything is peachy

   ```shell
   python setup.py test
   ```

1. Set up the feature, fix, or documentation branch.

   It is recommended to use the format [issue#]-[type]-[description] (e.g. 13-fix-connection-bug)

   ```shell
   git checkout -b 13-feature-new-stuff
   ```

1. Code and Commit!

   Here's a quick checklist for ensuring a good diff:

   - The diff touches the minimal amount of files possible while still fufilling the purpose of the diff
   - The diff uses Unix line endings
   - The diff adheres to our PEP8 style guides. If you've cloned the repo you can run `pycodestyle .`

1. Add Tests

1. Update Documentation

   Our documentation is written in markdown and built with [Mkdocs](http://www.mkdocs.org). More information on how to update and build the docs can be found [here](#updating-documentation)

1. Run the tests again and make sure they pass!

1. Submit to your fork

1. Submit a PR

1. Wait for a review, and address any feedback.

<!--
### Updating Documentation

### Running Tests
-->

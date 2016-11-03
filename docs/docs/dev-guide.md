---
title: Developer Guide
layout: docs
---

## Submitting your first patch

1. Make sure you have [signed the CLA](http://tableau.github.io/#contributor-license-agreement-cla)

1. Fork the repository.

   We follow the "Fork and Pull" model as described [here](https://help.github.com/articles/about-collaborative-development-models/).

1. Clone your fork:

   ```shell
   git clone http://github.com/<your_username>/document-api-python
   ```

1. Run the tests to make sure everything is peachy:

   ```shell
   python setup.py test
   ```

1. Set up the feature, fix, or documentation branch.

   It is recommended to use the format issue#-type-description (e.g. 13-fix-connection-bug) like so:

   ```shell
   git checkout -b 13-feature-new-stuff
   ```

1. Code and commit!

   Here's a quick checklist for ensuring a good pull request:

   - Only touch the minimal amount of files possible while still accomplishing the goal.
   - Ensure all indentation is done as 4-spaces and your editor is set to unix line endings.
   - The code matches PEP8 style guides. If you cloned the repo you can run `pycodestyle .`
   - Keep commit messages clean and descriptive.
     If the PR is accepted it will get 'Squashed' into a single commit before merging, the commit messages will be used to generate the Merge commit message.

1. Add tests.

   All of our tests live under the `test/` folder in the repository.  
   We use `unittest` and the built-in test runner `python setup.py test`.  
   If a test needs a static file, like a twb/twbx, it should live under `test/assets/`

1. Update the documentation.

   Our documentation is written in markdown and built with Jekyll on Github Pages. All of the documentation source files can be found in `docs/docs`.

   When adding a new feature or improving existing functionality we may ask that you update the documentation along with your code.

   If you are just making a PR for documentation updates (adding new docs, fixing typos, improving wording) the easiest method is to use the built in `Edit this file` in the Github UI

1. Submit to your fork.

1. Make a PR as described [here](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) against the 'development' branch.

1. Wait for a review and address any feedback.
   While we try and stay on top of all issues and PRs it might take a few days for someone to respond. Politely pinging the PR after a few days with no response is OK, we'll try and respond with a timeline as soon as we are able.

1. That's it! When the PR has received :rocket:'s from members of the core team they will merge the PR

<!--
### Updating Documentation

### Running Tests
-->

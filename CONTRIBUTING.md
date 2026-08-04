# Contributing to DataMind AI

First off, thank you for considering contributing to DataMind AI! It's people like you that make DataMind AI such a great tool.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](https://github.com/YOUR_USERNAME/DataMind_AI/issues) page to see if someone else has already created a ticket. If not, go ahead and [make one](https://github.com/YOUR_USERNAME/DataMind_AI/issues/new)!

## 2. Fork & create a branch

If this is something you think you can fix, then fork DataMind AI and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-text-to-sql-tool
```

## 3. Implementation Guidelines

- Ensure you have activated your virtual environment before installing dependencies.
- Follow PEP 8 guidelines for Python code formatting.
- Make sure to add docstrings to any new functions or classes.
- Update `requirements.txt` if you introduce any new dependencies.

## 4. Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with DataMind AI's master branch:

```sh
git remote add upstream git@github.com:YOUR_USERNAME/DataMind_AI.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout 325-add-text-to-sql-tool
git rebase master
git push --set-upstream origin 325-add-text-to-sql-tool
```

Finally, go to GitHub and make a Pull Request. 🎉

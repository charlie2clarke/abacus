## Contribution
To navigate the codebase it is likely that you will need to be familiar with the following main libraries:
- Python HTTPServer (https://docs.python.org/3/library/http.server.html)
- Python Azure Service Bus Client (https://pypi.org/project/azure-servicebus/)

### Issues
If you spot a problem with the code, [search if an issue already exists](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments). If a related issue doesn't exist, you can open a new issue using a relevant [issue template](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments).

### Make changes
Makes changes in a local supporting branch using the following naming convention:
```
<feature/bug/hotfix>/<issue number>-<hyphenated description of change>
```

Once you have completed your changes, commit them with a message following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) specification.

Push your changes to the supporting branch.

Then you can open a pull request:
- Link the pull request to the issue you are resolving.
- Assign a reviewer (this is mandatory)
- Changes may be asked to be made before you can merge your pull request.
- As you update your pull request and apply changes, mark each conversation as resolved.
- Your pull request will trigger a pipeline to run tests and linting on your code to ensure it meets quality constraints. You will not be able to merge your changes until all of these have passed.

### Your pull request is merged!
Thanks for your contribution.

# Event Processor
Event processor subscribes to an Azure Service Bus to receive, process, and format sensor and actuator data suitable for charting. 

## Motivation
When subscribing to an Azure Service Bus details can be exposed which should be hidden from the client. Using this also allows for dumb-ui approach to be taken.

## Setup
It is preferable that a virtualenv is created. 

### Virtualenv
https://docs.python.org/3/library/venv.html

To create a venv run:
```
$ python -m venv venv
```

For Windows (using Powershell) run:
```
$ venv\Scripts\Activate.ps1
```

For Mac/Linux run:
```
$ source venv/bin/activate
```

### Requirements
```
$ pip install -r requirements.txt
```

### Azure Service Bus
Event processor depends on subscribing to values from an existing Azure Service Bus. To connect to your Azure Service Bus, set the following environment variables:
```
SERVICEBUS_CONNECTION_STR
SERVICEBUS_SENSOR_TOPIC
SERVICEBUS_ACTUATOR_TOPIC
SERVICEBUS_SUBSCRIPTION_NAME
```

### Run
To run the application, use the following:
```
$ python src/main/app.py --profile dev
```

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


# to_slack

Send messages to Slack from Python. You'll need to [get hooks from Slack](https://api.slack.com/tutorials/slack-apps-hello-world) for each user or channel. Each hook is a string. They look like this:

> https://hooks.slack.com/services/X03SU38LS/B7JT9RT6D/rRSoP986AkaZ5capZyyXOgJx

You just need the part after `https://hooks.slack.com/services/`. So, for the above hook, just `X03SU38LS/B7JT9RT6D/rRSoP986AkaZ5capZyyXOgJx`.

```python
from to_slack import To

to = To({
    'sally': '<hook>',
    'david': '<hook>',
    'general': '<hook>'
})

# send a message to sally
to.sally('Hello')

# send a message to sally and david
to.sally.david('Hello')

# send a message to sally and david and the general channel
to.sally.david.general('Hello')

# etc.

```

You specify each target for the message via dot notation, after the `To` instance. Targets are flushed after a message is sent, but you can freeze them:

```python

from to_slack import freeze

to_peeps = freeze(to.sally.david)

to_peeps('hey')
to_peeps('grass')
```

## wait, I have a `.` in my username

Sure:

```python
from to_slack import To

to = To({
    'no.regrets': '<hook>'
})

# send a message to no.regrets
to.no.regrets('Hello')

# this will fail
to.no('Hello')  # Exception: Invalid target: "no".

# so will this
to.no.regets.man('Hello')  # Exception: Invalid target: "man".
```

## wait, I have a `-` in my username

That's more problematic, but ok:

```python
from to_slack import To

to = To({
    'no.regrets': '<hook>',
    'sam': '<hook>',
    'so-hyphen': '<hook>'
})

to['so-hyphen'].sam.no.regrets('hi all')
```

## what if I don't know who to send to until run time?

```python
from to_slack import To

to = To({
    'no.regrets': '<hook>',
    'sam': '<hook>',
    'so-hyphen': '<hook>'
})

recipients = ['no.regrets', 'sam', 'so-hypen']

to[recipients]('still no regrets')
```

## installation

 * copy this file wherever you like (sorry, no PyPI)
 * install requests, or `pip install -r requirements.txt`

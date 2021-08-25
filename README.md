# pybsub
## simple python pubsub stuff based on asyncio and uvloop

Install required packages
```
pip3 install requirements.txt
```

Run `app.py` to starting unix server

Publish a message to specific channel by executing:
```
python3 publish_script.py <channel_name> <message string>
```
Subscribe specific channel by executing:
```
python3 subscribe_script.py <channel_name>
```

## TODO
- [ ] Add logging
- [ ] Support multiple channel subscribtion
- [ ] Publishing a message to multiple channel
- [ ] Better Argument Parsing
- [ ] Persist messages

# Speakup-Bot
This is a very simple bot for [SpeakUp](https://web.speakup.info/home) that allows to send multiple threads to answer the same question.

## Setup

### You'll need:
- Python. I know python 3.10 to work but I don't know exactly what is the minimum version that is needed.
- [selenium](https://www.selenium.dev/): there's a `requirements.txt` file that you can use to install it using pip (`pip install -r requirements.txt`)

### To run:

``` bash
python3 bot.py <target> <opt> <nb_threads>
```

where:
- `target`: is the link to the poll, i.e. something like "https://web.speakup.info/room/join/XXXX"
- `opt`: is the answer you want the bots to vote for. I.e. "A", "B",...
- `nb_threads`: is the number of bots that you want to send. I.e. the number of votes you want to cast

### Example:

The following code:

```bash
python3 bot.py https://web.speakup.info/room/join/XXXXX B 10
```

will send 10 new votes to option B on the most recent poll at "https://web.speakup.info/room/join/XXXXX"

---


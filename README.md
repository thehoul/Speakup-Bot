# Speakup-Bot
This is a very simple bot for [SpeakUp](https://web.speakup.info/home) that allows to send multiple threads to answer the same question.

## Setup

Here we have two options. The second one is highly recommended because it will be able to send large amount of requests whereas the first will struggle to launch more than 15 votes.

### Option 1:
Using selenium to vote

**Requirements**:

- Python. I know python 3.10 to work but I don't know exactly what is the minimum version that is needed.
- [selenium](https://www.selenium.dev/): there's a `requirements.txt` file that you can use to install it using pip (`pip install -r requirements.txt`)

**To run:**

``` bash
python3 bot.py <target> <answer> <nb_threads>
```

where:
- `target`: is the link to the poll, i.e. something like "https://web.speakup.info/room/join/XXXX"
- `answer`: is the answer you want the bots to vote for. I.e. "A", "B",...
- `nb_threads`: is the number of bots that you want to send. I.e. the number of votes you want to cast

**Example:**

The following code:

```bash
python3 bot.py https://web.speakup.info/room/join/25330 B 10
```

will send 10 new votes to option B on the most recent poll at "https://web.speakup.info/room/join/25330"


### Option 2:
Using socket programing to talk directly with the server

**Requirements**:

- Python. I know python 3.10 to work but I don't know exactly what is the minimum version that is needed.
- [tqdm](https://tqdm.github.io/): there's a `requirements.txt` file that you can use to install it using pip (`pip install -r requirements.txt`)

**To run:**

``` bash
python3 socketbot.py <room_id> <answer> <nb_threads>
```

where:
- `room_id`: is the id of the room, i.e. something like "25330"
- `answer`: is the answer you want the bots to vote for. I.e. "A", "B",...
- `nb_threads`: is the number of bots that you want to send. I.e. the number of votes you want to cast

**Example:**

The following code:

```bash
python3 socketbot.py 25330 B 10
```

will send 10 new votes to option B on the most recent poll in room 25330

---


import requests
import json
import sys
import threading
import argparse
from tqdm import tqdm
from store import Store
# Number of arguments for the script
NB_ARGS = 3

# Load JSON request templates
JOIN_TEMPLATE = json.load(open('./requests_templates/join_template.json'))
VOTE_TEMPLATE = json.load(open('./requests_templates/vote_template.json'))
AUTH_TEMPLATE = json.load(open('./requests_templates/auth_template.json'))
VALIDATE_KEY_TEMPLATE = json.load(open('./requests_templates/validate_template.json'))

# API endpoints
AUTH = 'https://web.speakup.info/speakup/api/auth/login'
VALIDATE_KEY = 'https://web.speakup.info/speakup/api/room/validateJoinKey'
GRAPHQL = 'https://web.speakup.info/speakup/graphql'


def prepare_templates(room_id):
    JOIN_TEMPLATE['variables']['joinKey'] = str(room_id)
    VALIDATE_KEY_TEMPLATE['joinKey'] = str(room_id)

def load_json(template_path):
    with open(template_path) as f:
        return json.load(f)

def authenticate():
    response = requests.post(AUTH, json=AUTH_TEMPLATE)
    resp_json = response.json()
    token = resp_json['accessToken']
    return token

def join_room(id, key, token):
    '''
    response = requests.post(VALIDATE_KEY, json=VALIDATE_KEY_TEMPLATE, headers={"Authorization": str(token)})
    if response.json()['ok'] == False:
        print(f"Thread {id}: Couldn't join room...")
        return None
    '''
    response = requests.post(GRAPHQL, json=JOIN_TEMPLATE, headers={"Authorization": f"Bearer {token}"})

    return response.json()

def get_poll(id, attendee_json):
    polls = attendee_json['data']['roomAttendee']['room']['polls']

    # Find first open poll
    open_poll = None
    for poll in polls:
        if poll['isOpened'] == True:
            open_poll = poll
            break

    if open_poll == None:
        print(f"Thread {id}: No open poll found")
        return None
    else:
        return open_poll

def vote_answer(id, poll, answer, token):
    options = poll['options']

    vote_id = None
    for opt in options:
        if opt['label'].lower() == answer.lower():
            vote_id = opt['id']
            break
    
    if vote_id == None:
        print(f"Thread {id}: Couldn't find option {answer}")
        return None

    # Send post request to vote
    query = VOTE_TEMPLATE.copy()
    # Modify poll ID to match current poll
    query['variables']['pollId'] = poll['id']
    # Modify option ID to match selected option
    query['variables']['checkedOpId'] = vote_id
    # Send query
    response = requests.post(GRAPHQL, json=query, headers={"Authorization": f"Bearer {token}"})
    # Check if vote was successful
    resp_json = response.json()
    if resp_json['data']['pollOptionResult']['isChecked'] == True:
        return True
    else:
        return False


def run(id, room_id, answer, pb, store):
    while store.get_job():
        # Authenticate
        token = authenticate()
        pb.update()
        # Join the room
        resp_json = join_room(id, room_id, token)
        pb.update()
        # Get the poll
        poll = get_poll(id, resp_json)
        pb.update()
        # Vote
        if vote_answer(id, poll, answer, token):
            pb.update()

parser = argparse.ArgumentParser(description='Vote on a poll in a SpeakUp room')
parser.add_argument('room_id', metavar='room_id', type=int, help='The room ID')
parser.add_argument('answer', metavar='answer', type=str, help='The answer to vote for')
parser.add_argument('nb_votes', metavar='nb_votes', type=int, help='The number of votes to perform')
parser.add_argument('-t', dest='nb_threads', action='store', type=int, default=1, help='The number of threads to use')

args = parser.parse_args()

room_id = args.room_id
answer = args.answer
nb_votes = args.nb_votes
nb_threads = args.nb_threads
vote_per_thread = int(nb_votes / nb_threads)

store = Store(nb_votes)

print(f"Casting {nb_votes} votes in {nb_threads} threads")
print(f"Voting for {answer} in room {room_id}\n")

prepare_templates(room_id)
pb = tqdm(total=nb_votes*4)

threads = list()
for index in range(nb_threads):
    x = threading.Thread(target=run, args=(index, room_id, answer, pb, store))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()

pb.close()
el = pb.format_dict["elapsed"]
print()
print(f"Finished all jobs in {el:0.3f} seconds", flush=True)
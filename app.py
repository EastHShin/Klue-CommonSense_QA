from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from flask import Flask, request, jsonify, render_template
import torch
import torch.nn.functional as F
from queue import Queue, Empty
from threading import Thread
import time

app = Flask(__name__)

print("model loading...")

tokenizer = AutoTokenizer.from_pretrained("EasthShin/Klue-CommonSense-model")
model = AutoModelForQuestionAnswering.from_pretrained("EasthShin/Klue-CommonSense-model")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

print("complete model loading")

def handle_requests_by_batch():
    while True:
        request_batch = []

        while not(len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:
                try:
                    requests["output"] = make_answer(requests["input"][0], requests["input"][1])
                except Exception as e:
                    requests["output"] = e


handler = Thread(target=handle_requests_by_batch).start()

def make_answer(context, question):
    try:
        encodings = tokenizer(context, question, max_length=512, truncation=True,
                              padding="max_length", return_token_type_ids=False)
        encodings = {key: torch.tensor([val]) for key,val in encodings.items()}

        input_ids = encodings["input_ids"].to(device)
        attention_mask = encodings["attention_mask"].to(device)
        pred = model(input_ids, attention_mask=attention_mask)
        start_logits, end_logits = pred.start_logits, pred.end_logits
        token_start_index, token_end_index = F.softmax(start_logits).argmax(dim=-1), F.softmax(end_logits).argmax(dim=-1)
        answer_ids = input_ids[0][token_start_index:token_end_index + 1]

        answer = tokenizer.decode(answer_ids)
        result = dict()
        result[0] = answer

        return result

    except Exception as e:
        print('Error occur in script generating!', e)
        return jsonify({'error': e}), 500

@app.route('/generate', methods=['POST'])
def generate():
    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'Error': 'Too Many Requests'}), 429

    try:
        args = []
        context = request.form['context']
        question = request.form['question']

        args.append(context)
        args.append(question)

    except Exception as e:
        return jsonify({'message': 'Invalid request'}), 500

    req = {'input': args}
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])

@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return "Clear", 200

@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200

@app.route('/')
def main():
    return render_template('index.html'), 200

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
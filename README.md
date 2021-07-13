# Klue-CommonSense_QA

---
[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/EastHShin/Klue-CommonSense_QA)

---

Try using the QA model as a BERT model trained on CommonSense Data from [Mindslab](https://mindslab.ai:8080/kr/company)

Github: [KLUE-benchmark/KLUE](https://github.com/KLUE-benchmark/KLUE)
<br>
<br>
Open Api: [On Ainize](https://ainize.ai/EastHShin/Klue-CommonSense_QA?branch=main)
<br>
<br>
License: [CC-BY-SA-4.0](https://github.com/KLUE-benchmark/KLUE/blob/main/License.md)
<br>
<br>
Model: [HuggingFace](https://huggingface.co/EasthShin/Klue-CommonSense-model)
<br>
<br>
Code: [Ainize Workspace](https://ainize.ai/workspace/create?imageId=hnj95592adzr02xPTqss&git=https://github.com/EastHShin/Klue-CommonSense-workspace)
### Post parameter
```
context: 질문에 답할 수 있는 문맥
question: 질문
```

### Output format
```
{"0": 답변}
```

## With CLI

---
### Input example
```
curl -X POST "https://main-klue-common-sense-qa-east-h-shin.endpoint.ainize.ai/generate" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "context={}" -F "question={}"
```

### Output example
```
{
    "0": {}
}
```
### API Health Check
```
$ curl --request GET "https://main-klue-common-sense-qa-east-h-shin.endpoint.ainize.ai/healthz"
{
  Health
}
```

## With a Demo

---
Demo page: [End-point](https://main-klue-common-sense-qa-east-h-shin.endpoint.ainize.ai)
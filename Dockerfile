FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-devel

WORKDIR /app
RUN pip install flask transformers torch
COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000 
ENTRYPOINT ["python"]
CMD ["./views.py"]

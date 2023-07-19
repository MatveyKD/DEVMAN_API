FROM python:3-onbuild
EXPOSE 5000
RUN pip install -r requirements.txt
COPY /devman_api .
CMD ["python", "./main.py"]

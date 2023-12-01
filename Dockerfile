FROM python:3
ADD MishaBot.py /
ADD requirements.txt /
RUN python -m pip install -r ./requirements.txt
CMD [ "python", "./MishaBot.py" ]
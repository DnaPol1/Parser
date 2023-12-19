FROM python:3
ADD MishaBot.py /
ADD scraping.py /
ADD requirements.txt /
RUN python -m pip install -r ./requirements.txt
CMD [ "python", "./MishaBot.py", "./scraping.py" ]
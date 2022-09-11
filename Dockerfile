FROM python:3.9
COPY . .
RUN pip install mysql-connector-python pandas pydantic pysimplegui
CMD ["python", "main_code.py"]
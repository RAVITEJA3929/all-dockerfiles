FROM python
LABEL this is from ubuntu image
MAINTAINER name ravi teja kanchanapally
WORKDIR /teja/
COPY . .
EXPOSE 8501
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "finance_tracker.py"]



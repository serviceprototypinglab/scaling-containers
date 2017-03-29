FROM python:2-onbuild
#ENV CYCLOPS_ENDPOINT=localhost:port/data
ENV DATABASE_HOST=mongo
ENV DATABASE_PORT=27017
EXPOSE 55555
ENTRYPOINT ["python","/usr/src/app/backend.py"]
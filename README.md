# Application based in microservices architecture.

The application simulate a document management application.
There two micro-services:

- database_mongo: It is the stateful micro-services and it is a
MongoDB database  of documents in which each document belongs to
a user (tenant). And it is ready to be scaled with a replication 
of the micro-service and the data or with a partition of the data.

- documents_crud: It is a stateless micro-service: It is a CRUD 
for documents, with the option to search patterns in the documents
as well. This service provides a REST API implemented in Python. 
 
- Data: It is for generate the data used in the database.
It is an array of JSON structures which represent the documents 
and can be generated using ./Data/GenerateData.py
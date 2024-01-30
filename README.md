# lambda-dynamodb-api_gateway-integration

### Architecture
![image](https://github.com/ankitgupta14011998/lambda-dynamodb-api_gateway-integration/assets/32798626/ef3b069c-e963-4d79-90b8-5b42e426b660)

### Steps

1. Create DynamoDB table with primary key.
2. create lambda function with python runtime 3.8.
3. create API gateway and configure sources(/health,/products,/product etc.)
4. add the request CRUD operations(GET,POST,PATCH,DELETE etc.)
5. create the stage area where API will load the data.
6. use lambda proxy integrations with lambda function created above.
7. use the attached python code as lambda function.
8. invoke the API url in API_Gateway stage page and run it in postman
9. you may optionally configure API key and secret key, permission and security feature.

You can play around by using RDS instead of DynamoDB, or dump data in snowflake or Redshift for analytics

refer this youtube link for reference
!https://www.youtube.com/watch?v=Ut5CkSz6NR0

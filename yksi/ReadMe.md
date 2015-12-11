# Yksi Example Django

Leveraging:
* Django 1.9
* Python 3
* Bootstrap
* Asynchronous tasks with celery and RabbitMQ
* S3 compatible (EMC ECS) storage backend
* Social Authentication
* Cloud Foundry

## Installation

Simplest way to test this app is to use ``Vagrant`` with ``vagrant up``. This will create a Fedora Virtualbox with all required packages and a python virtual environment.

## Configuration

### modify environments file for development
copy "environments.sh.example" environments.sh
modify environments.sh

### ECS

#### create ecs access keys
https://portal.ecstestdrive.com/

#### create buckets and corresponding CORS configuration (example below)
```
<CORSConfiguration>
 <CORSRule>
   <AllowedOrigin>http://www.example.com</AllowedOrigin>
   <AllowedMethod>PUT</AllowedMethod>
   <AllowedMethod>POST</AllowedMethod>
   <AllowedMethod>DELETE</AllowedMethod>
   <AllowedHeader>*</AllowedHeader>
 </CORSRule>
 <CORSRule>
   <AllowedOrigin>*</AllowedOrigin>
   <AllowedMethod>GET</AllowedMethod>
 </CORSRule>
</CORSConfiguration>
```
#### collectstatic at client
python manage.py collectstatic

### create social authentication

#### Google:
https://console.developers.google.com/

##### Create application
Creat OAuth 2 Credentials -> Web application -> Authorized redirect URIs: http://app.domain.com/complete/google-oauth2/
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = Client secret
```
##### Enable API
Overview -> Google+ API -> Enable API

#### Twitter:
https://apps.twitter.com/

##### Create application
Create New App -> Callback URL: http://app.domain.com/complete/twitter/
```
SOCIAL_AUTH_TWITTER_KEY = Consumer Key (API Key)
SOCIAL_AUTH_TWITTER_SECRET = Consumer Secret (API Secret)
```
#### cloud foundry

##### login to Cloud Foundry
```cf login -a https://api.run.pivotal.io```

##### create services
```
cf create-service elephantsql turtle yksi_db
cf create-service cloudamqp lemur yksi_rabbitmq
cf cups appname_ecs -p '{"HOST":"object.ecstestdrive.com","ACCESS_KEY_ID":"1234567890@ecstestdrive.emc.com","SECRET_ACCESS_KEY":"1234567890","PUBLIC_URL":"1234567890.public.ecstestdrive.com"}'
cf cups appname_mail -p '{"HOST":"smtp.domain.local","USER":"django@domain.local","PASSWORD":"1234567890","PORT":"25","TLS":"True"}'
cf cups appname_socialauth -p '{"TWITTER_KEY":"1234567890","TWITTER_SECRET":"1234567890","GOOGLE_KEY":"1234567890.apps.googleusercontent.com","GOOGLE_SECRET":"1234567890"}'
```
##### initial push for database creation or later database migrations
```cf push --no-route -c "bash ./init_db.sh" -i 1```

##### push app
```cf push```

##### push celery
```cf push -f manifest-celery.yml```

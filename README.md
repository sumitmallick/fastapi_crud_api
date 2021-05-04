This is a crud api built on fastapi with postgresql db

Process to run the app:

1. If you want to run it on local:
    a. Create a virtual environment: 
        python3 -m venv env
        p.s. - Please use Python version >=3.8
    
    b. Activate the virtual environment:
        source env/bin/activate
    
    c. Install required packages:
        pip3 install -r requirements.txt
    
    d. Run the app with this command:
        uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 8000
        p.s - For this method please create a postgres db from your local pgadmin, named as fastapi_crud

    e Check your app on 0.0.0.0:8000/docs

2. If you want to run it as a docker container:
    a. create a .env file in backend folder and add these lines with your secrect keys and values respectively:
        """
        SECRET_KEY=your_secrect_key
        POSTGRES_USER=postgres_username
        POSTGRES_PASSWORD=postgres_password
        POSTGRES_SERVER=server_name
        POSTGRES_PORT=port_id
        POSTGRES_DB=db_name
        """
    b. Run this command if you docker installed in local:
        docker-compose up

        -- This command will automatically run your app on 0.0.0.0:8000/docs and one app container and one db container will be created

3. Check this app on production:
    http://198.50.215.181:8000/docs

How to use the app:

    a. There are multiple parts and their features are given as api endpoints in the swagger ui

    b. First create a user from users part --> 
        Go to /api/users/ and create a json as given in example with your email_id, username, password and hit execute button to post the api
        Use authorize button to login with the given email_id as username and password
    
    c. Now try & use all the apis as per given instructions and example query params if required
        p.s - Some apis doesn't need to be authorized by users

Deployment:

As this application is already dockerized we can use any cloud platform to deploy it.
p.s. - As heroku itself creates such containerized env I haven't deploy it on heroku

It is directly hosted on a server as an uvicorn app where after allocating an ip you just have to clone the repo and run docker-compose up(make sure docker is already available or installed in the server) and it will easily run as a production server

I haven't used any dns as for the same dns there is already an app is running and I am running this app on different ip

Scaling:

For such moments or cases where we are getting increasing page hits and it looks like the app can not handle it as it's current configuration then
if we are deploying it on any server we can deploy multiple instances of the app to spin up on multiple ips of same dns and add load balancer to be automatically scaled so that load balancer can distribute the requests' loads equally.

How this works: every ip or every instance of the app will work like a different machine and when any page request comes for the dns it will first go to
the load balancer and it will transfer the requests to the ips according to the load. 

There are two types of load balancer, physical and application and here we can use physical one. For nginx we can use it's default load balancer or we can use services like elb(Elastic Load Balancing) of aws.

Now after these here comes the bottleneck cases of dbs. We can do here partitioning of dbs and there can be multiple ways to do that we can use this as per our suitability. It will help us to handle higher db table calls. We can also use db sharding but as per my thinking we don't need it if we want to handle around 15 million users for this type of application.

If these much also doesn't helps then we can add caching layer in between primary db and backend server. If I will get a call for any particular request we can add it first in the cache. We can use redis or kafka for that. It will add values in cache which serves way faster than primary db and moreover we will add a cronjob to call it after every predefined time duration to sync the primary db with cache. Usecase: For this case if I will get multiple calls to retrieve the rating of any movie which has recently released then for that calling the primary db again & again is a very bad idea and here we can use caching. So we can serve all of these from cache and gets faster api responses.

Please let me know if you find out any changes required.
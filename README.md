# Description

Projects consists of 3 applications:
- TENANTS - tenant management - adding, deploying, removing a tenant
- APP - this is the actual app which each tenant will use
- USERS - defines common user model for both above

Each tenant application has its own database and subdomain.


## How to run the project

```sh
./reset.sh
```
will spin up the whole project.
In order to run tests:

```sh
docker compose exec web pytest
```

## User Guide
### Log in to Tenants Management App
Deployed project does not have any tenants configured yet.
Only tenants management app is accessible. 
A superuser is automatically created for this app:
> **Note:** Each superuser created in tenants management app is mirrored in the dedicated tenants app

**http://localhost/tenants/**   user **admin** password **admin**

![img.png](images/img.png)

### Create a new tenant
![add-tenant.png](images/add-tenant.png)

In order to deploy the tenant app, select deploy action and run it.
![deploy.png](images/deploy.png)
![img_1.png](images/img_1.png)
After that, refresh multiple times, so that "SETTINGS LOADED" always appear as True 

> **Note:** There are 4 gunicorn server workers to be reloaded, so sometimes it can show False after True

Once deployed and new settings are loaded, we can run db migration:
![img_2.png](images/img_2.png)
![img_3.png](images/img_3.png)

Now you can use the link on the right side to access tenants app with same admin credentials:
http://yahoo.localhost/application

Under Customers, you can create tenants app users (superuser created here will not be mirrored anywhere else)
![img_4.png](images/img_4.png)
> **Important:** API token is created automatically and visible in users record

### API
In order to authenticate, include token in request headers:
```
-H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

API paths:

    subdomain.localhost/
        /api-token-auth/
        /api/
        /api/<drf_format_suffix:format>/
        /api/departments/
        /api/departments/<pk>/ 
        /api/departments/<pk>.<format>/
        /api/departments.<format>/
        /api/organizations/
        /api/organizations/<pk>/ 
        /api/organizations/<pk>.<format>/
        /api/organizations.<format>/



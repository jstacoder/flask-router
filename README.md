### Flask-Router

#### Features:
  + Combine your blueprints routes into a `urls.py` file
  + Can register unknown blueprints that provide routes by setting `REGISTER_BLUEPRINTS` to True
  + All of your route definitions in one place
  + Unlike Django no regex knowlegde needed to define routes<br/>(although it is using regex you just dont have to care)
  + standard, easy to remember, route definition syntax
    - Using class-based-views: `( (bp,),(url,endpoint,view) )`
        
        ```python
            from .views import MainView, SubView
            from . import app_blueprint

            routes = (
                (app_blueprint,),
                ('/','main',MainView),
                ('/sub','sub',SubView),
            )
        ```
    - Using view functions: `( (bp,), (url,view_func) )`
        ```python
            from .views import main_view, sub_view
            from . import app_blueprint

            routes = (
                (app_blueprint,),
                ('/',main_view),
                ('/sub',sub_view),
            )
        ```

#### To Use:
  * `pip install flask-router`
  * then import it:  

  ```python  
    from flask_router import FlaskRouter
  ```  

  * Then setup your app:
    - standard way, ie: w/o factory pattern: 

    ```python
        router = FlaskRouter(app)
    ```  

    - w/factory pattern:  

    ```python
        router = FlaskRouter()
    ```  

    then later  

    ```python
        router.init_app(app)
    ```  





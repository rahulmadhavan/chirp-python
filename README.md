=============
# chirp-python
=============

to discover services using chirp on the same network

## Installation


```pip install chirp-python ```  OR  ```easy_install chirp-python```

## Example:


**PREREQUISITES:**  *running the example requires Flask web framework,
        install the [Flask](http://flask.pocoo.org/) module before executing the example*

* execute the following commands
  
  - ```python example/chirpy.py chirper1 9001 &```
  - ```python example/chirpy.py chirper2 9002 &```
  - open [http://localhost:9001/chirpers](http://localhost:9001/chirpers), you will see that chirper1 has discovered chirper2, the response should be as follows
   
  
  ```json   
      {
        "chirper2": {
            "config": {},
            "uri": "chirp.org",
            "protocol": "http",
            "name": "chirper2",
            "port": "9002"
        }
      }
```

  - Also if you, open [http://localhost:9002/chirpers](http://localhost:9002/chirpers), you will see that chirper2 has discovered chirper1, the response should be as follows

  ```json   
    {
        "chirper1": {
            "config": {},
            "uri": "chirp.org",
            "protocol": "http",
            "name": "chirper1",
            "port": "9001"
        }
    }
  ```

- now execute

    ``` python example/chirpy.py chirper3 9003 &```

  - and open

    - [http://localhost:9001/chirpers](http://localhost:9001/chirpers)
    - [http://localhost:9002/chirpers](http://localhost:9002/chirpers)
    - [http://localhost:9003/chirpers](http://localhost:9003/chirpers)
      

  - you will see that they have all discovered each other
  - To understand the apis provided by chirp have a look at the [example/chirpy.py](example/chirpy.py)
      
      
      
**HOST**
----
  https://inobtenio.dev/

**Return plot image URL**
----
  Returns the URL where a plot image lives

* **URL**

  /projects/covid-19/plot?command=command&country=country&days=days

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `command=[string]`one of (total|new|deaths|recovered)
   `country=[string]`
   `days=[string|integer]`must be in the [0,7] (inclusive) range

* **Data Params**

  None

**Return API info**
----
  Returns info about the API such as author and data sources

* **URL**

  /projects/covid-19/info

* **Method:**

  `GET`
  
*  **URL Params**
  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : ok, message : "info text" }`
 

**Error Responses:**
----

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{{
    "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
    "documentation": {
        "handlers": {
            "/plot": {
                "GET": {
                    "usage": " Returns the plot image URL in the format {'status': 'ok', 'message': 'url.to/plot/image'}\n    Accepted values for <command> are: (total|new|deaths|recovered)\n    <days> must be in the (0,8) range. This includes 0 and 7.",
                    "examples": [
                        "http://127.0.0.1/plot?command=total&country=chile&days=2",
                        "http://127.0.0.1/plot?command=recovered&country=united+kingdom&days=0"
                    ],
                    "outputs": {
                        "format": "JSON (Javascript Serialized Object Notation)",
                        "content_type": "application/json; charset=utf-8"
                    },
                    "inputs": {
                        "command": {
                            "type": "Basic text / string value"
                        },
                        "country": {
                            "type": "Basic text / string value"
                        },
                        "days": {
                            "type": "Basic text / string value",
                            "default": 0
                        }
                    }
                }
            },
            "/info": {
                "GET": {
                    "usage": "Returns the plot image URL in the format {'status': 'ok', 'message': 'large text'}",
                    "examples": [
                        "http://127.0.0.1/info"
                    ],
                    "outputs": {
                        "format": "JSON (Javascript Serialized Object Notation)",
                        "content_type": "application/json; charset=utf-8"
                    }
                }
            }
        }
    }
}}`

  OR

  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Content:** `{ errors: { error : "Error message" } }`

  OR

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ errors: { error : "Error message" } }`

* **Sample Calls:**

  ```javascript
  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "https://inobtenio.dev/projects/covid-19/plot/?command=total&country=chile&days=0",
    "method": "GET"
  }

  $.ajax(settings).done(function (response) {
    console.log(response);
  });
  ```

  ```python
  import requests

  url = "https://inobtenio.dev/projects/covid-19/plot/"
  querystring = {"command":"total","country":"chile","days":"0"}

  response = requests.request("GET", url, params=querystring)
  print(response.text)
  ```

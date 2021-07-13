# ClassifyIT #

* A service for Classification of Images and Texts

## Installation ##
* Docker image

## Usage ##
```
POST /classifyit HTTP/1.1
Host: <docker_host>:5000
Content-Type: application/json
{
    "image_url": "<image_URL>",
    "image_texts": [
        "text 1",
        "text 2",
        "text 3",
        ...
    ]
}
```

## Credits ##

* Danny Briskin (dbriskin@qaconsultants.com)

## License ##
[MIT](https://opensource.org/licenses/MIT)

## 3rd party licenses ##
|Component|License|Link|
|---------|-------|----|
|CLIP|[MIT](https://opensource.org/licenses/MIT)|[License](https://github.com/openai/CLIP/blob/main/LICENSE)|

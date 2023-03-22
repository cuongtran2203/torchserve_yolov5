**Build docker from docker file**

> ```
> docker build -t vds .
> ```

**Runining service** 

```
docker run --rm -it -p 8080:8080 -p 8081:8081 vds torchserve --start --model-store service/model-store --models Cuong2203=Cuong2203.mar --ts-config service/config.properties
```

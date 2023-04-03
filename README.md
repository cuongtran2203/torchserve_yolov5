**Build docker from docker file**

> ```
> docker build -t vds .
> ```

**Runining service**

```
docker run --rm -it -p 8080:8080 -p 8081:8081 -p 7070:7070 -p 7071:7071 vds 
```

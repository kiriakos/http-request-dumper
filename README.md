# HTTP Request Dumper

Listens on the specified port and dumps all incomming requests to a file.

## Usage

Clone and Start the service

```bash
docker build -t http-request-dumper .
mkdir -p /tmp/reqdump
docker run --rm -v/tmp/reqdump:/requests -p8011:8080 http-request-dumper
```

In another terminal do

```bash
curl --include -d"FOOBAR" localhost:8011/foo/bar
```

Now look at `/tmp/reqdump`

## Known Limitations
### Wrong Duplicate Headers

Python's `http.server` doesn't handle duplicate headers well.

```
curl -H"FOO: BAR" -H"FOO: ZZZ" 'localhost:8011'
```

will cause the http dump to be:

```http
GET /
Host: localhost:8011
User-Agent: curl/8.2.1
Accept: */*
FOO: BAR
FOO: BAR
```

Note that the `FOO` header exists twice but its value is `BAR` both times...

## Advanced

### Custom UID GID

By default this container runs as `1000:1000` and the username `python`.
You can change that by passing the `UID` and `GID` build arguments in the
build step.


### Flat files

By default requests are added in subdirectories based on the path that
is being requested. Eg: `curl localhost:8011/foo/bar` would created the
subdirectories `foo/bar` and put request files in there.

This behavior can be changed on execution by passing the `--flat` argument
at the end of the `run` command. eg:

```bash
docker build -t http-request-dumper .
mkdir -p /tmp/reqdump
docker run --rm -v/tmp/reqdump:/requests -p8011:8080 http-request-dumper --flat
```

### Other runtime flags

The project also offers the `--port` and `--address` flags but as container
execution is much more convenient, please refrain from using them.

## Provenance

Inspired by the [httpd-reflector](https://gist.github.com/amotl/3ed38e461af743aeeade5a5a106c1296) gist.

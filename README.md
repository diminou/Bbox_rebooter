# Auto rebooter for Boygues Telecom's Bbox

## How it works

It calls the test web page hosted behind the Bbox to see whether it is reachable from the outisde. If it is not, it reboots the box. The test is done every 30 seconds; if the Bbox is unreachable itself, the script does nothing for 30 seconds.

In order to configure the script, add a `params.json` file to the folder with the following contents:

```
{"baseUrl":"http://192.168.1.254",
"testUrl":"<test_web_page_address>",
"password":"<Bbox's password>"}
```

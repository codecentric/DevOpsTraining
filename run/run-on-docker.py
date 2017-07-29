import sys, traceback
import docker
import BaseHTTPServer
import time
import urlparse

client = docker.from_env()

HOST_NAME = '0.0.0.0'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000  # Maybe set this to 9000.
DNS = sys.argv[1]

print HOST_NAME, PORT_NUMBER, DNS

PORT_MAP = {}
PORT_MAP['blue'] = 18000
PORT_MAP['green'] = 19000

LABELS_BLUE={"traefik.backend" : "blue", "traefik.frontend.rule" : "Host:localhost:80"}
LABELS_GREEN={"traefik.backend" : "green", "traefik.frontend.rule" : "Host:localhost:80"}

LABELS_MAP = {"blue" : LABELS_BLUE, "green": LABELS_GREEN}


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        try:
            message = "OK"
            parsed = urlparse.urlparse(self.path)

            print parsed
            print urlparse.parse_qs(parsed.query)

            environment = urlparse.parse_qs(parsed.query)['environment'][0]
            dockerName = 'env-' + urlparse.parse_qs(parsed.query)['environment'][0]

            applicationUrl = urlparse.parse_qs(parsed.query)['application'][0]

            version = urlparse.parse_qs(parsed.query)['version'][0]

            otherEnvironment = self.getOtherEnvironment(environment)
            self.disableLoadBalancing(otherEnvironment)

            print("parsed query params")

            print environment, DNS, applicationUrl, version, otherEnvironment

            self.cleanupContainer(dockerName)

            traceback.print_exc(file=sys.stdout)
            print("unable to stop container")

            labels = LABELS_MAP[environment]
            labels['traefik.enabled'] = "true"

            client.containers.run('hylke1982/openjdk-download-and-run',
                                  command=[applicationUrl, "--environment=" + environment, "--version=" + version],
                                  name=dockerName,
                                  detach=True,
                                  network="servicediscovery_default",
                                  labels=labels,
                                  ports={'24242/tcp': PORT_MAP[environment]},
                                  dns=[DNS])

        except:
            traceback.print_exc(file=sys.stdout)
            message = "NOK"

        self.wfile.write(message)
        self.finish()
        return

    def getOtherEnvironment(self, environment):
        otherEnvironment = "blue"
        if environment == 'blue':
            otherEnvironment = "green"
        return otherEnvironment

    def cleanupContainer(self, environment):
        try:
            container = client.containers.get(environment);
            container.stop()
            container.remove()
        except:
            print "No container could be stopped"

    def disableLoadBalancing(self, otherEnvironent):
        try:
            container = client.containers.get(otherEnvironent);
            labels = LABELS_MAP[otherEnvironent]
            labels['traefik.enabled'] = "false"
            container.reload()
        except:
            print "No container could be updated"



    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        self.wfile.close()
        self.rfile.close()


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

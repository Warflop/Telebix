import requests

class ZabbixAPIGraph:
    def __init__(self, server, username, password):
        self.debug = False
        self.server = server
        self.username = username
        self.password = password
        self.proxies = {}
        self.verify = True
        self.cookie = None
        self.tmp_dir = None

    def login(self):

        data_api = {"name": self.username, "password": self.password, "enter": "Sign in"}
        req_cookie = requests.post(self.server + "/", data=data_api, proxies=self.proxies, verify=self.verify)
        cookie = req_cookie.cookies
        if len(req_cookie.history) > 1 and req_cookie.history[0].status_code == 302:
            print_message("probably the server in your config file has not full URL (for example "
                          "'{0}' instead of '{1}')".format(self.server, self.server + "/zabbix"))
        if not cookie:
            print_message("authorization has failed, url: {0}".format(self.server + "/"))
            cookie = None

        self.cookie = cookie

    def do_graph(self, graphid, tmp_dir):

        file_img = tmp_dir + "/{0}.png".format(graphid)

        zbx_img_url = self.server + "/chart2.php?graphid={0}".format(graphid)

        if self.debug:
            print_message(zbx_img_url)
        res = requests.get(zbx_img_url, cookies=self.cookie, proxies=self.proxies, verify=self.verify, stream=True)
        res_code = res.status_code
        if res_code == 404:
            print_message("can't get image from '{0}'".format(zbx_img_url))
            return False
        res_img = res.content
        with open(file_img, 'wb') as fp:
            fp.write(res_img)

        return file_img

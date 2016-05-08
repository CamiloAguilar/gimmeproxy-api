#!/usr/bin/env python
# -*- coding: utf-8 -*-u

"""
author = efourrier

Purpose : this is a small python wrapper for
"""


#########################################################
# Import Packages and helpers
#########################################################

import os
import json
import pickle
import requests

from .exceptions import Invalid


# apikey = os.environ.get('PROXY_API_KEY')

# maxResults is 250 maximum

# default_parameters = {'apiKey':apikey,'onlyActive':True,'onlyHttps':True,'onlyHighAvailLowLatency':True,
# 					#'onlySupportsGoogle':True,'onlySupportsAmazon':True,
# 					# 'onlySupportsCraigslist':True,'onlySupportsTripAdvisor':True,'onlySupportsKayak':True,
# 					'minimumUptimePercentage':99,#'countryCodes':"US",
# 					'onlyHighAnonymity':True,'maxResults':250,'sortByLatestTest':True}


#########################################################
# Main functions
#########################################################

class GimmeProxyApi(object):
    """ This is a class to get proxies via the gimmeproxy api and process them
    in order to get the right format for the proxies parameter of the requests package """
    _nb_calls_per_min_limit = 20
    nb_total_calls = 0
    parameters_name = ["apikey", "get", "post", "cookies", "referer", "user-agent",
     "supportsHttps", "anonymityLevel", "protocol", "port", "country", "maxCheckPeriod"]
    parameters_value = ["string", "true/false", "true/false", "true/false", "true/false",
      "true/false", "0/1", "http/socks4/socks5", "integer", "string", "integer, seconds"]
    parameters_description = ["API key, if you have one, allows to scrape faster", "GET requests support", "POST requests support",
     "Cookies support", "referer header support", "user-agent header support",
      "HTTPS support", "Anonymity level, 1 - anonymous, 0 - not anonymous",
       "Proxy protocol", "Proxy port", "Return only proxies with specified country",
        "Return only proxies checked in last maxCheckPeriod seconds"]
    def __init__(self, apikey=None):
        self.apikey = apikey
        if self.apikey is None:
            print("You have no api key you are limited to {} calls per minute").format(
                self._nb_calls_per_min_limit)
        self.base_url="http://gimmeproxy.com/api/getProxy"
        self.custom_params={'get': True, 'supportsHttps': True, 'anonymityLevel': 1,
                              'maxCheckPeriod': 300, 'supportsHttps': True, 'user-agent': True,
                              'protocol': 'http'}

    def get_infos_parameters(self):
        """ Returns a dict infos with as key parameter and values a dict with values and description """
        zip_params = zip(self.parameters_name,
                         self.parameters_value, self.parameters_description)
        infos_params = {}
        for (n, v, d) in zip_params:
            infos_params[n] = {'value': v, "description": d}
        return infos_params

    def _check_params(self, params):
        """ Check that a dict of parameters are valid for the api """
        params_names = params.keys()
        for k in params_names:
            if k not in self.parameters_name:
                raise BadParameters(
                    "Additionnal parameters should be in {}".format(self.parameters_name))

    def get_proxies(self,**kwargs):
        """
        add additionnal parameter to the api call (we put params = default_parameters)

        Arguments
        ---------
        **kwargs : to add additionnal parameters to request example :
        g = GimmeProxyApi()
        g.get_proxies(country="US")
        g.get_proxies(g.custom_params)

        Returns
        -------
        raw json response from the api

        """
        self._check_params(kwargs)
        r = requests.get(self.base_url, params=kwargs)
        if r.ok:
            json_response = r.json()
        else:
            print("Something went wrong ...")
        self.nb_total_calls += 1
        return json_response

        def reset(self):
            """ Reset nb_total_calls """
            self.nb_total_calls = 0


# if __name__ == "__main__":
# 	gp = GetProxies(apikey=apikey)
# 	proxy_world = gp.get_proxies(save_json="list_https_world_proxies3.json")
# 	proxies_dict_world = gp.process_json_dict(proxy_world,save_file="list_https_world_proxies_test.p")
# 	proxy_us = get_proxies(default_parameters,save_json="list_https_us_proxies.json",countryCodes="US")
# 	process_json(proxy_us,save_file="list_https_us_proxies.txt")
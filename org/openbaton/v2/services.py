import logging

from org.openbaton.v2.cmd import BaseObCmd
from org.openbaton.v2.utils import get_result_to_list, get_result_to_show, parse_path_or_json, result_to_str


class Services(BaseObCmd):
    """Command to manage Services. It allows to:
        * show details of a specific Service passing an id
        * list all saved Services
        * delete a specific Service passing an id
        * create a specific Service passing a path to a file or directly the json content
    """

    log = logging.getLogger(__name__)
    keys_to_list = ["id", "name"]
    keys_to_exclude = []

    def find(self, params):
        if not params:
            return "ERROR: missing <service-id>"
        _id = params[0]
        return result_to_str(get_result_to_show(self.app.ob_client.get_service(_id),
                                                     excluded_keys=self.keys_to_exclude,
                                                     _format=self.app.format))

    def create(self, params):
        if not params:
            return "ERROR: missing <service> or <path-to-json>"

        service_str = "".join(params)
        self.log.debug("String service is %s" % service_str)
        service = parse_path_or_json(service_str)
        return self.app.ob_client.create_service(service)

    def delete(self, params):
        if not params:
            return "ERROR: missing <servicename>"
        _id = params[0]
        self.app.ob_client.delete_service(_id)
        return "INFO: Deleted service with id %s" % _id

    def list(self, params=None):
        return result_to_str(
            get_result_to_list(self.app.ob_client.list_services(), keys=self.keys_to_list, _format=self.app.format),
            _format=self.app.format)

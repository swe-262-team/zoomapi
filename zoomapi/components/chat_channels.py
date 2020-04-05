"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi import util
from zoomapi.components import base

class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    def list(self, **kwargs):
        return self.get_request(
            "/chat/users/me/channels"
        )

    def create(self, **kwargs):
        util.require_keys(kwargs, "name")
        return self.post_request(
            "/chat/users/me/channels"
        )
    
    def get(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.get_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), params=kwargs
        )

    def update(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.patch_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), params=kwargs
        )

    def delete(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.delete_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), params=kwargs
        ) 
    
    def list_members(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.get_request(
            "/chat/channels/{}/members".format(kwargs.get("channelId")), params=kwargs
        )
    
    def invite(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.post_request(
            "/chat/channels/{}/members".format(kwargs.get("channelId")), params=kwargs
        )

    def join(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.post_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channelId")), params=kwargs
        )

    def leave(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.delete_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channelId")), params=kwargs
        )
    
    def remove(self, **kwargs):
        util.require_keys(kwargs, ["channelId","memberId"])
        return self.delete_request(
            "/chat/channels/{}/members/{}".format(kwargs.get("channelId"), kwargs.get("memberId")), params=kwargs
        )
        

    



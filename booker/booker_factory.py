# -*- coding: utf-8 -*-
from _9C.spring_airlines import SpringAirlines
from _ZE.eastar_jet import EastarJet
from _IT.tigerair_tw import TigerAirTw


class BookerFactory(object):

    @staticmethod
    def newBooker(req):
        if req.ipcc == '9C_F':
            return SpringAirlines()
        if req.ipcc == 'ZE_F':
            return EastarJet()
        if req.ipcc == 'IT_F':
            return TigerAirTw()
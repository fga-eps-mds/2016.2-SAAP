# coding=utf-8
from default.views import *
import pytest


def test_checar_campos():
    campos = ['teste']
    response = checar_campos(campos)
    assert response is True

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PharmacieProduit(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id_produit: int=None, prix: int=None, disponible: int=None):  # noqa: E501
        """PharmacieProduit - a model defined in Swagger

        :param id_produit: The id_produit of this PharmacieProduit.  # noqa: E501
        :type id_produit: int
        :param prix: The prix of this PharmacieProduit.  # noqa: E501
        :type prix: int
        :param disponible: The disponible of this PharmacieProduit.  # noqa: E501
        :type disponible: int
        """
        self.swagger_types = {
            'id_produit': int,
            'prix': int,
            'disponible': int
        }

        self.attribute_map = {
            'id_produit': 'id_produit',
            'prix': 'prix',
            'disponible': 'disponible'
        }
        self._id_produit = id_produit
        self._prix = prix
        self._disponible = disponible

    @classmethod
    def from_dict(cls, dikt) -> 'PharmacieProduit':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Pharmacie_produit of this PharmacieProduit.  # noqa: E501
        :rtype: PharmacieProduit
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_produit(self) -> int:
        """Gets the id_produit of this PharmacieProduit.


        :return: The id_produit of this PharmacieProduit.
        :rtype: int
        """
        return self._id_produit

    @id_produit.setter
    def id_produit(self, id_produit: int):
        """Sets the id_produit of this PharmacieProduit.


        :param id_produit: The id_produit of this PharmacieProduit.
        :type id_produit: int
        """

        self._id_produit = id_produit

    @property
    def prix(self) -> int:
        """Gets the prix of this PharmacieProduit.


        :return: The prix of this PharmacieProduit.
        :rtype: int
        """
        return self._prix

    @prix.setter
    def prix(self, prix: int):
        """Sets the prix of this PharmacieProduit.


        :param prix: The prix of this PharmacieProduit.
        :type prix: int
        """

        self._prix = prix

    @property
    def disponible(self) -> int:
        """Gets the disponible of this PharmacieProduit.


        :return: The disponible of this PharmacieProduit.
        :rtype: int
        """
        return self._disponible

    @disponible.setter
    def disponible(self, disponible: int):
        """Sets the disponible of this PharmacieProduit.


        :param disponible: The disponible of this PharmacieProduit.
        :type disponible: int
        """

        self._disponible = disponible

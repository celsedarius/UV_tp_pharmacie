# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.centre import Centre  # noqa: E501
from swagger_server.models.medecin import Medecin  # noqa: E501
from swagger_server.models.pharmacie import Pharmacie  # noqa: E501
from swagger_server.models.produit import Produit  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_hosto_add(self):
        """Test case for hosto_add

        ajouter un centre de sante
        """
        query_string = [('centre', Centre())]
        response = self.client.open(
            '/hosto',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hosto_del(self):
        """Test case for hosto_del

        supprimer un centre de santé
        """
        response = self.client.open(
            '/hosto/{hostoID}'.format(hosto_id='hosto_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hosto_edit(self):
        """Test case for hosto_edit

        modifier un centre de sante
        """
        query_string = [('hosto', Centre())]
        response = self.client.open(
            '/hosto/{hostoID}'.format(hosto_id='hosto_id_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hosto_ls(self):
        """Test case for hosto_ls

        liste des centres de santeé
        """
        response = self.client.open(
            '/hosto',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hosto_proche(self):
        """Test case for hosto_proche

        les centres de santé proche de vous
        """
        query_string = [('long', 1.2),
                        ('lat', 1.2)]
        response = self.client.open(
            '/hosto_proche',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medecin_add(self):
        """Test case for medecin_add

        ajouter médecin
        """
        query_string = [('medecin', Medecin())]
        response = self.client.open(
            '/medecin',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medecin_del(self):
        """Test case for medecin_del

        supprimer un medecin
        """
        response = self.client.open(
            '/medecin/{medecinID}'.format(medecin_id='medecin_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medecin_edit(self):
        """Test case for medecin_edit

        modifier details d'un medecin
        """
        query_string = [('medecin', Medecin())]
        response = self.client.open(
            '/medecin/{medecinID}'.format(medecin_id='medecin_id_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medecin_ls(self):
        """Test case for medecin_ls

        listes des medecins
        """
        response = self.client.open(
            '/medecin',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medicament_add(self):
        """Test case for medicament_add

        ajouter un medicament
        """
        query_string = [('produit', Produit())]
        response = self.client.open(
            '/medicament',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medicament_del(self):
        """Test case for medicament_del

        supprimer medicament
        """
        response = self.client.open(
            '/medicament/{medicamentID}'.format(medicament_id='medicament_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medicament_edit(self):
        """Test case for medicament_edit

        supprimer un medicament
        """
        query_string = [('produit', Produit())]
        response = self.client.open(
            '/medicament/{medicamentID}'.format(medicament_id='medicament_id_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medicament_equivalent(self):
        """Test case for medicament_equivalent

        medicament equivalent dans les pharmacies proches de vous
        """
        query_string = [('long', 1.2),
                        ('lat', 1.2),
                        ('medicament', 'medicament_example')]
        response = self.client.open(
            '/equivalent',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_medicament_ls(self):
        """Test case for medicament_ls

        liste des medicaments
        """
        response = self.client.open(
            '/medicament',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_add(self):
        """Test case for pharmacie_add

        ajouter une pharmacie
        """
        query_string = [('pharmacie', Pharmacie())]
        response = self.client.open(
            '/pharmacie',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_del(self):
        """Test case for pharmacie_del

        supprimer une pharmacie
        """
        response = self.client.open(
            '/pharmacie/{pharmacieID}'.format(pharmacie_id='pharmacie_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_garde(self):
        """Test case for pharmacie_garde

        centre de sante a cote de nous
        """
        query_string = [('long', 1.2),
                        ('lat', 1.2)]
        response = self.client.open(
            '/pharmacie_garde',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_ls(self):
        """Test case for pharmacie_ls

        listes des pharmacies
        """
        response = self.client.open(
            '/pharmacie',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_proche(self):
        """Test case for pharmacie_proche

        listes des pharmacies proche de vous
        """
        query_string = [('long', 1.2),
                        ('lat', 1.2)]
        response = self.client.open(
            '/pharmacie_proche',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pharmacie_update(self):
        """Test case for pharmacie_update

        modifier detail d'une pharmacie
        """
        query_string = [('pharmacie', Pharmacie())]
        response = self.client.open(
            '/pharmacie/{pharmacieID}'.format(pharmacie_id='pharmacie_id_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_recherche_medicament(self):
        """Test case for recherche_medicament

        centre de sante a cote de nous
        """
        query_string = [('long', 1.2),
                        ('lat', 1.2),
                        ('medicament', 'medicament_example')]
        response = self.client.open(
            '/recherche_medicament',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

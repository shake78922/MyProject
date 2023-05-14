from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import RcpTable
from django.urls import reverse

class RcpTableListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcplist = []
        for i in range(15):
            for j in range(1,6):
                self.rcplist.append(RcpTable.objects.create(rcp_pk=((i*5)+j), rcp_num=(i+1), rcp_sub_num=j, rcp_nm=f"Recipe {i+1}", rcp_ingrdnt_nm=f"Ingredient {i+1}-{j}"))

    def test_retrieve_table_list(self):
        response = self.client.get(reverse('RecipeApp:table_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RecipeApp/rcptable_list.html')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['table_list']), 10)
        for i in range(len(self.rcplist)):
            self.assertEqual(self.rcplist[i].rcp_pk, i+1)
        for i in range(15):
            for j in range(1,6):
                index = ((i*5)+(j-1))
                self.assertEqual(self.rcplist[index].rcp_num, i+1)
                self.assertEqual(self.rcplist[index].rcp_sub_num, j)
                self.assertEqual(self.rcplist[index].rcp_nm, f"Recipe {i+1}")
                self.assertEqual(self.rcplist[index].rcp_ingrdnt_nm, f"Ingredient {i+1}-{j}")
        
class RcpNmListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcplist = []
        for i in range(15):
            for j in range(1,6):
                self.rcplist.append(RcpTable.objects.create(rcp_pk=((i*5)+j), rcp_num=(i+1), rcp_sub_num=j, rcp_nm=f"Recipe {i+1}", rcp_ingrdnt_nm=f"Ingredient {i+1}-{j}"))

    def test_retrieve_table_list(self):
        response = self.client.get(reverse('RecipeApp:rcp_nm_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RecipeApp/rcp_nm_list.html')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['rcp_nm_list']), 10)
        last_rcp_num = 15*5
        for i in range(last_rcp_num, last_rcp_num-10, -1):
            index = last_rcp_num-i
            rcp_num = 18-(3+index)
            self.assertEqual(response.context['rcp_nm_list'][index].rcp_num, rcp_num)
            self.assertEqual(response.context['rcp_nm_list'][index].rcp_nm, f'Recipe {rcp_num}')
        
class RcpDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='test_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_nm="Test Recipe",rcp_ingrdnt_nm="Test Ingredient")

    def test_retrieve_rcp_detail(self):
        response = self.client.get(reverse('RecipeApp:rcp_detail', kwargs={'rcp_num': self.rcp.rcp_num}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RecipeApp/rcp_detail.html')
        self.assertEqual(response.context['rcp_detail'][0].rcp_nm, "Test Recipe")
        self.assertEqual(response.context['rcp_detail'][0].rcp_ingrdnt_nm, "Test Ingredient")


class RcpUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_nm="Test Recipe", rcp_ingrdnt_nm="Test Ingredient")

    def test_update_rcp(self):
        response = self.client.post(reverse('RecipeApp:rcp_update', kwargs={'rcp_num': self.rcp.rcp_num}), {'rcp_nm_1': 'Updated Recipe', 'rcp_ingrdnt_nm_1': 'Updated Ingredient'})
        self.assertEqual(response.status_code, 302)
        updated_rcp = RcpTable.objects.get(rcp_num=self.rcp.rcp_num)
        self.assertEqual(updated_rcp.rcp_nm, 'Updated Recipe')
        self.assertEqual(updated_rcp.rcp_ingrdnt_nm, 'Updated Ingredient')


class IngrdntCreateView(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_nm="Test Recipe", rcp_sub_num=1, rcp_sub_nm='Test Stage Name1', rcp_ingrdnt_nm="Test Ingredient1")

    def test_create_ingrdnt(self):
        response = self.client.post(reverse('RecipeApp:ingrdnt_create', kwargs={'rcp_num': self.rcp.rcp_num}), {'rcp_sub_num': (self.rcp.rcp_sub_num + 1), 'rcp_sub_nm': 'Test Stage Name2', 'rcp_ingrdnt_nm': 'Test Ingredient2'})
        self.assertEqual(response.status_code, 302)
        new_ingrdnt = RcpTable.objects.get(rcp_num=self.rcp.rcp_num, rcp_sub_num=(self.rcp.rcp_sub_num + 1))
        self.assertEqual(new_ingrdnt.rcp_sub_nm, 'Test Stage Name2')
        self.assertEqual(new_ingrdnt.rcp_ingrdnt_nm, 'Test Ingredient2')
        

class RcpCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_nm="Test Recipe", rcp_ingrdnt_nm="Test Ingredient")

    def test_create_rcp(self):
        response = self.client.post(reverse('RecipeApp:rcp_create'), {'rcp_nm': 'New Recipe', 'rcp_ingrdnt_nm': 'New Ingredient'})
        self.assertEqual(response.status_code, 200)
"""        new_rcp = RcpTable.objects.create(rcp_num=(self.rcp.rcp_num + 1), rcp_nm="New Recipe", rcp_ingrdnt_nm="New Ingredient")
        self.assertEqual(new_rcp.rcp_nm, 'New Recipe')
        self.assertEqual(new_rcp.rcp_ingrdnt_nm, 'New Ingredient')"""


class IngrdntDeleteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_sub_num=1, rcp_nm="Test Recipe", rcp_sub_nm="Test Stage Name1", rcp_ingrdnt_nm="Test Ingredient1")
        self.ingrdnt = RcpTable.objects.create(rcp_pk=2, rcp_num=1, rcp_sub_num=(self.rcp.rcp_sub_num + 1), rcp_sub_nm="Test Stage Name1", rcp_ingrdnt_nm="Test Ingredient2")

    def test_delete_ingrdnt(self):
        response = self.client.post(reverse('RecipeApp:ingrdnt_delete', kwargs={'pk': self.rcp.rcp_pk, 'rcp_num': self.rcp.rcp_num}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RcpTable.objects.filter(rcp_pk=self.rcp.rcp_pk).exists())


class RcpDeleteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create_user(username='testcode_name', password='testcode_pw')
        test_user.save()
        self.rcp = RcpTable.objects.create(rcp_pk=1, rcp_num=1, rcp_nm="Test Recipe", rcp_ingrdnt_nm="Test Ingredient")

    def test_delete_rcp(self):
        response = self.client.post(reverse('RecipeApp:rcp_delete', kwargs={'rcp_num': self.rcp.rcp_num}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RcpTable.objects.filter(rcp_num=self.rcp.rcp_num).exists())
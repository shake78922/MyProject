# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    msmt = models.CharField(max_length=50, blank=True, null=True)
    rcp = models.ForeignKey('Recipe', models.CASCADE, related_name = 'ingredient')
    
    def __str__(self):
        return "[재료] " + self.name

    class Meta:
        db_table = 'ingredient'


class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return "[레시피] " + self.name

    class Meta:
        db_table = 'recipe'


class RcpTable(models.Model): # Recipe , Ingredient, field에서 rcp_ , num , nm 변수이름 변경
    rcp_pk = models.AutoField(db_column='RCP_PK', primary_key=True)  # Field name made lowercase.
    rcp_num = models.IntegerField(db_column='RCP_NUM', blank=True, null=True)  # Field name made lowercase.
    rcp_nm = models.CharField(db_column='RCP_NM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcp_sub_num = models.IntegerField(db_column='RCP_SUB_NUM', blank=True, null=True)  # Field name made lowercase.
    rcp_sub_nm = models.CharField(db_column='RCP_SUB_NM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcp_ingrdnt_nm = models.CharField(db_column='RCP_INGRDNT_NM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcp_ingrdnt_qnt = models.CharField(db_column='RCP_INGRDNT_QNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rcp_ingrdnt_unit = models.CharField(db_column='RCP_INGRDNT_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rcp_ingrdnt_sub = models.CharField(db_column='RCP_INGRDNT_SUB', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return "[" + self.rcp_nm + "] " + self.rcp_ingrdnt_nm
        
    class Meta:
        db_table = 'rcp_table'

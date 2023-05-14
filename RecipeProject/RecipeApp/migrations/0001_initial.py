# Generated by Django 4.2 on 2023-05-02 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RcpTable',
            fields=[
                ('rcp_pk', models.AutoField(db_column='RCP_PK', primary_key=True, serialize=False)),
                ('rcp_num', models.IntegerField(blank=True, db_column='RCP_NUM', null=True)),
                ('rcp_nm', models.CharField(blank=True, db_column='RCP_NM', max_length=100, null=True)),
                ('rcp_sub_num', models.IntegerField(blank=True, db_column='RCP_SUB_NUM', null=True)),
                ('rcp_sub_nm', models.CharField(blank=True, db_column='RCP_SUB_NM', max_length=100, null=True)),
                ('rcp_ingrdnt_nm', models.CharField(blank=True, db_column='RCP_INGRDNT_NM', max_length=100, null=True)),
                ('rcp_ingrdnt_qnt', models.CharField(blank=True, db_column='RCP_INGRDNT_QNT', max_length=50, null=True)),
                ('rcp_ingrdnt_unit', models.CharField(blank=True, db_column='RCP_INGRDNT_UNIT', max_length=50, null=True)),
                ('rcp_ingrdnt_sub', models.CharField(blank=True, db_column='RCP_INGRDNT_SUB', max_length=50, null=True)),
            ],
            options={
                'db_table': 'rcp_table',
            },
        ),
    ]

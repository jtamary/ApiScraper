from django.db import models

  
class BillType(models.Model):
    bill_type_id = models.IntegerField()
    bill_type_id.primary_key = True
    bill_type_name = models.CharField(max_length = 1000)
    bill_type_desc = models.CharField(max_length = 1000)
    

class BillData(models.Model):
    bill_id = models.IntegerField()
    bill_id.primary_key = True
    bill_number = models.IntegerField(null=True)
    bill_name = models.CharField(max_length = 1000)
    bill_sub_number = models.IntegerField(null=True, blank=True)
    # bill_type_id = models.ForeignKey(BillType)
    bill_type_id = models.IntegerField(null=True, blank=True)
    bill_file_link = models.CharField(max_length = 1000)
    
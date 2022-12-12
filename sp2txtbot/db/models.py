from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    tag = fields.CharField(max_length=255, unique=True, null=True)
    username = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.username


class Recognition(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='recognitions', on_delete=fields.CASCADE)
    file_id = fields.CharField(max_length=512, unique=True)
    recognized_text = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'Recognition {self.id}'

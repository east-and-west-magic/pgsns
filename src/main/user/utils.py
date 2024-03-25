from .models import CustomUser


def export_user_to_json():
    # q=CustomUser.objects.create(key="value") # 插入数据
    q = list(q)
    for i in q:
        print(i.email)
        print(i.password)
        print(i.username)
        # todo: 写入json文件

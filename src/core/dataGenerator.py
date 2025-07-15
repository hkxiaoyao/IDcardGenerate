# coding:utf-8
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import os
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw
import numpy as np
import random
from ..data.dictionary import alphabet, nations
from ..data.address_set import province_set, city_set, couty_set
from .dataAugmentation import augment

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *


wordWidth = 70
wordHeight = 100
boxes = {'name': [400, 680, 1000, 780],
         'sex': [400, 820, 720, 920],
         'nation': [830, 820, 1380, 920],
         'sex_nation': [400, 820, 1380, 920],
         'birthday': [400, 960, 1330, 1060],
         'addr': [400, 1100, 1400, 1200],
         'idn': [400, 1450, 1800, 1550]}
images_output_path = './data/images/'
txt_output_path = './data/annotations/'
dict_sum = len(alphabet) + 1

if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'usedres')
else:
    base_dir = os.path.join(os.path.dirname(__file__), 'usedres')

def IDcard_generator(amount):
    name_all = []
    sex_all = []
    nation_all = []
    addr_all = []
    year_all = []
    mon_all = []
    day_all = []
    id_all = []
    others = []

    numbers = '0123456789'
    
    # 常见姓氏
    common_surnames = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', 
                       '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
                       '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧']
    
    # 常见名字字符
    common_name_chars = ['明', '华', '建', '文', '军', '国', '强', '民', '伟', '峰',
                         '磊', '涛', '超', '辉', '宇', '杰', '浩', '志', '勇', '鹏',
                         '娟', '英', '玲', '芳', '燕', '雯', '萍', '红', '慧', '静',
                         '美', '丽', '秀', '敏', '艳', '莉', '梅', '琳', '君', '欣']

    for i in range(amount):
        # 改进姓名生成：姓氏+1-2个名字字符
        surname = random.choice(common_surnames)
        name_length = random.randint(1, 2)
        given_name = ''.join(random.sample(common_name_chars, name_length))
        name_all.append(surname + given_name)

        result = random.sample(u'男女', 1)
        sex_all.append(''.join(result))

        result = random.sample(nations, 1)
        nation_all.append(''.join(result))

        # 修复年份生成：1950-2010年合理范围
        year = random.randint(1950, 2010)
        year_all.append(str(year))

        # 修复月份生成：01-12月
        month = random.randint(1, 12)
        mon_all.append(f"{month:02d}")

        # 修复日期生成：考虑月份天数
        if month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif month in [4, 6, 9, 11]:
            max_day = 30
        else:  # 2月
            max_day = 28
        day = random.randint(1, max_day)
        day_all.append(f"{day:02d}")

        id = []
        addr = []
        province = random.sample(province_set, 1)[0]
        # province = [u'天津市', 12]
        addr += province[0]
        if province[0] in city_set.keys():
            city = random.sample(city_set[province[0]], 1)[0]
            addr += city[0]
            if city[0][0] in couty_set.keys():
                couty = random.sample(couty_set[city[0]], 1)
                addr += couty[0]
                id += str(couty[1])
            else:
                id += str(city[1])
                if len(id) == 4:
                    id += random.sample(numbers, 2)
        else:
            id += str(province[1])
            if len(id) == 2:
                id += random.sample(numbers, 4)
        addr = ''.join(addr)
        # 优化地址：移除随机字符填充，保持真实地址
        if len(addr) > 20:  # 如果地址太长，适当截取
            addr = addr[:20]
        
        # 修复身份证号生成：使用新的年月日
        id += str(year)
        id += f"{month:02d}"
        id += f"{day:02d}"
        id += random.sample(numbers, 3)
        id += random.sample(u'0123456789X', 1)
        addr_all.append(addr)
        id_all.append(''.join(id))

    return name_all, sex_all, nation_all, year_all, mon_all, day_all, addr_all, id_all

def generator(num):
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn
    images = []
    for i in range(num):
        name = ename[i]
        sex = esex[i]
        nation = enation[i]
        year = eyear[i]
        mon = emon[i]
        day = eday[i]
        addr = eaddr[i]
        idn = eidn[i]

        im = PImage.open(os.path.join(base_dir, 'fore.png'))

        name_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 72)
        other_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 60)
        bdate_font = ImageFont.truetype(os.path.join(base_dir, 'fzhei.ttf'), 60)
        id_font = ImageFont.truetype(os.path.join(base_dir, 'ocrb10bt.ttf'), 72)

        draw = ImageDraw.Draw(im)
        draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), sex, fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), nation, fill=(0, 0, 0), font=other_font)
        draw.text((630, 980), year, fill=(0, 0, 0), font=bdate_font)
        draw.text((950, 980), mon, fill=(0, 0, 0), font=bdate_font)
        draw.text((1150, 980), day, fill=(0, 0, 0), font=bdate_font)
        start = 0
        loc = 1120
        while start + 11 < len(addr):
            draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            loc += 100
        draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
        draw.text((950, 1475), idn, fill=(0, 0, 0), font=id_font)

        # im.save(output_path + 'color.png')
        # im.convert('L').save(output_path + 'bw.png')
        images.append(im.convert('L'))
        if (i+1) % 100 == 0:
            print('Generate images: {}/{}'.format(i+1, num))
        
    return images

def fragment_IDcard_save(images, augmented=False, batch_name=None):
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn
    txt_out = []
    num = len(images)
    if augmented:
        print('Output augmented data to {} and {}'.format(images_output_path, txt_output_path))
    else:
        print('Output data to {} and {}'.format(images_output_path, txt_output_path))
    for i in range(num):
        name = u'姓名' + ename[i]
        sex = u'性别' + esex[i]
        nation = u'民族' + enation[i]
        sex_nation = sex + nation
        birthday = u'出生' + eyear[i] + u'年' + emon[i] + u'月' + eday[i] + u'日'
        addr = u'住址' + eaddr[i]
        idn = u'公民身份证号码' + eidn[i]

        im = images[i]
        # name
        result = im.crop(boxes['name'])
        if augmented:
            result = augment(result)
        result.save(images_output_path + batch_name + str(i) + '_name.png')
        label = batch_name + str(i) + '_name.png ' + name + '\n'
        txt_out.append(label)
        if np.random.randint(0, 3) > 0:
            # sex
            result = im.crop(boxes['sex'])
            if augmented:
                result = augment(result)
            result.save(images_output_path + batch_name + str(i) + '_sex.png')
            label = batch_name + str(i) + '_sex.png ' + sex + '\n'
            txt_out.append(label)
            # nation
            result = im.crop(boxes['nation'])
            if augmented:
                result = augment(result)
            result.save(images_output_path + batch_name + str(i) + '_nation.png')
            label = batch_name + str(i) + '_nation.png ' + nation + '\n'
            txt_out.append(label)
        else:
            # sex and nation
            result = im.crop(boxes['sex_nation'])
            if augmented:
                result = augment(result)
            result.save(images_output_path + batch_name + str(i) + '_sex_nation.png')
            label = batch_name + str(i) + '_sex_nation.png ' + sex_nation + '\n'
            txt_out.append(label)
        # birthday
        result = im.crop(boxes['birthday'])
        if augmented:
            result = augment(result)
        result.save(images_output_path + batch_name + str(i) + '_birthday.png')
        label = batch_name + str(i) + '_birthday.png ' + birthday + '\n'
        txt_out.append(label)
        # address
        result = im.crop(boxes['addr'])
        if augmented:
            result = augment(result)
        result.save(images_output_path + batch_name + str(i) + '_addr.png')
        label = batch_name + str(i) + '_addr.png ' + addr + '\n'
        txt_out.append(label)
        # ID number
        result = im.crop(boxes['idn'])
        if augmented:
            result = augment(result)
        result.save(images_output_path + batch_name + str(i) + '_idn.png')
        label = batch_name + str(i) + '_idn.png ' + idn + '\n'
        txt_out.append(label)

        if (i+1) % 100 == 0:
            print('Output images: {}/{}'.format(i+1, num))

    with open(txt_output_path + 'data.txt', 'w') as f:
        for line in txt_out:
            f.write(line)

def IDcard_save(images, batch_name=None):
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn
    txt_out = []
    num = len(images)
    print('Output data to {} and {}'.format(images_output_path, txt_output_path))
    for i in range(num):
        name = u'姓名' + ename[i] + '\n'
        sex = u'性别' + esex[i]
        nation = u'民族' + enation[i]
        sex_nation = sex + nation + '\n'
        birthday = u'出生' + eyear[i] + u'年' + emon[i] + u'月' + eday[i] + u'日' + '\n'
        addr = u'住址' + eaddr[i] + '\n'
        idn = u'公民身份证号码' + eidn[i] + '\n'

        txt_out.append(batch_name + str(i) + '.png' + '\n')
        txt_out.append(name + sex_nation + birthday + addr + idn)
        images[i].save(images_output_path + batch_name + str(i) + '.png')

        if (i+1) % 100 == 0:
            print('Output images: {}/{}'.format(i+1, num))

    with open(txt_output_path + 'data.txt', 'w') as f:
        for line in txt_out:
            f.write(line)


def main(sample_sum=10, fragment_IDcard=False):
    """主函数：生成身份证数据
    
    Args:
        sample_sum: 生成样本数量，默认为10
        fragment_IDcard: 是否生成切片图片，默认为False
    """
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn
    
    print('--- Randomly Generate Content ---')
    ename, esex, enation, eyear, emon, eday, eaddr, eidn = IDcard_generator(sample_sum)
    print('--- Generate ID Card ---')
    images = generator(num=sample_sum)
    if fragment_IDcard:
        print('--- Fragment ID card ---')
        fragment_IDcard_save(images, augmented=True, batch_name='0_')
    else:
        print('--- ID card ---')
        IDcard_save(images, batch_name='0_')
    print('--- Generate Database Successfully ---')

if __name__ == '__main__':
    main(sample_sum=10, fragment_IDcard=False)

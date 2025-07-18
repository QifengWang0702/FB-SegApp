# -*- coding: UTF-8 -*-
import os
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm


def draw_title(title):
    style = getSampleStyleSheet()
    ct = style['Heading1']
    ct.fontName = 'TNRB'
    ct.fontSize = 18
    ct.leading = 30
    ct.alignment = 1
    ct.bold = True
    return Paragraph(title, ct)


def draw_img(path, width, height, align):
    img = Image(path)
    img.hAlign = align
    img.drawWidth = width * cm
    img.drawHeight = height * cm
    return img


def draw_text(text, fontName):
    style = getSampleStyleSheet()
    ct = style['Normal']
    ct.fontName = fontName
    ct.fontSize = 12
    ct.wordWrap = 'CJK'
    ct.alignment = 0
    ct.leading = 20
    return Paragraph(text, ct)


def draw_place(text):
    style = getSampleStyleSheet()
    ct = style['Normal']
    ct.fontName = 'TNR'
    ct.fontSize = 10
    ct.wordWrap = 'CJK'
    ct.alignment = 0
    ct.leading = 10
    ct.textColor = colors.white
    return Paragraph(text, ct)


def draw_table(width, height, chinese, *args):
    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'TNR'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black)]
    table = Table(args, colWidths=width, rowHeights=height, style=style)
    if chinese[0]:
        table.setStyle([('FONTNAME', (1, 0), (1, 0), 'ST')])
    if chinese[1]:
        table.setStyle([('FONTNAME', (1, 1), (1, 1), 'ST')])
    return table


def create(configs, reportId, visual_path, CArea, CLength, VArea, VLength, name, pregweek, docName, date, result,
           age, department='Obstetrics', gender='F'):
    TNR_path = os.path.join(configs['save']['configs'], configs['TTFont']['TNR'])
    TNRB_path = os.path.join(configs['save']['configs'], configs['TTFont']['TNRB'])
    ST_path = os.path.join(configs['save']['configs'], configs['TTFont']['ST'])
    pdfmetrics.registerFont(TTFont('TNR', TNR_path))
    pdfmetrics.registerFont(TTFont('TNRB', TNRB_path))
    pdfmetrics.registerFont(TTFont('ST', ST_path))

    CAreaScale = configs['segmentation']['normal']['CAreaScale']
    CLengthScale = configs['segmentation']['normal']['CLengthScale']
    VAreaScale = configs['segmentation']['normal']['VAreaScale']
    VLengthScale = configs['segmentation']['normal']['VLengthScale']
    pic_path = configs['save']['pic']
    logo = configs['picture']['hospital']

    content = []

    content.append(draw_title('Shengjing Hospital of China Medical University'))
    content.append(draw_img(f"{pic_path}/{logo}", 4, 1.5, 'CENTER'))
    content.append(draw_text(f'Check number: {reportId}', 'TNR'))

    data1 = [('Name: ', name, 'Age: ', age, 'Gender: ', gender, 'Pregweek:', pregweek),
             ('Department: ', department, 'Doctor: ', docName, 'Date: ', date, 'result: ', result)]
    chinese = [False, False]
    if re.match(r'^[A-Za-z]{1,64}$', name) is None:
        chinese[0] = True
    print(re.match(r'^(?![\u4e00-\u9fa5])[\da-zA-Z]{6,30}$', department))
    if re.match(r'^(?![\u4e00-\u9fa5])[\da-zA-Z]{6,30}$', department) is None:
        chinese[1] = True
    content.append(draw_table(65, 30, chinese, *data1))

    content.append(draw_place(' .'))
    str1 = 'Examination methods: Brain CT examination, prenatal ultrasound image intelligent recognition system automatically locates and segments CCC and CV.'
    content.append(draw_text(str1, 'TNR'))
    content.append(draw_place(' .'))
    content.append(draw_img(visual_path, 13, 8, 'CENTER'))

    content.append(draw_place(' .'))
    content.append(draw_text('unit: mm', 'TNR'))
    data2 = [('Inspection Item', 'Result(Area)', 'Reference(Area)', 'Result(Circum)', 'Reference(Circum)'),
             ('CCC', CArea, f'{CAreaScale[0]}~{CAreaScale[1]}', CLength, f'{CLengthScale[0]}~{CLengthScale[1]}'),
             ('CV', VArea, f'{VAreaScale[0]}~{VAreaScale[1]}', VLength, f'{VLengthScale[0]}~{VLengthScale[1]}')]
    content.append(draw_table(104, 40, [False, False], *data2))

    content.append(draw_place(' .'))
    str2 = 'Guidance: If the two values are greater than the normal value, fetal brain development abnormalities and other conditions may occur.'
    content.append(draw_text(str2, 'TNR'))
    content.append(draw_place(' .'))

    content.append(draw_place(' .'))
    content.append(draw_text("Doctor's signature:", 'TNRB'))

    return content


# create(123, 'Anny', 25, 10, 'Dan Zhao', '23.8.31', 'Normal',  'pic/dlut.png', 80, 70, 80, 70)

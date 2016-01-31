#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
from fetch_quotes import fetch_random_quote
import fetch_todo
import re, textwrap

WIDTH = 600
HEIGHT = 800
MARGIN_X = 15
MARGIN_Y = 10
EFFECTIVE_WIDTH = WIDTH - 2*MARGIN_X
LINE_SPACING = 4

def find_max_char_len(st, font):
    '''
    Find the largest character length we can make a paragraph using the given
    font object
    '''

    def find_max_char_recur(prev, end):
        if prev >= end:
            return prev - 1

        pivot = (prev+end) // 2

        q = st[0:pivot]
        line_width, _ = font.getsize(q)

        if line_width > EFFECTIVE_WIDTH:
            end = pivot - 1
            return find_max_char_recur(prev, end)
        elif line_width < EFFECTIVE_WIDTH:
            prev = pivot + 1
            return find_max_char_recur(prev,end)
        else:
            return pivot

    initial_line_width, _ = font.getsize(st)

    if initial_line_width <= EFFECTIVE_WIDTH:
        return len(st)
    else:
        start = 0
        end = len(st)
        return find_max_char_recur(start,end)

def render_paragraph(draw_obj, topy,string):
    font = ImageFont.truetype('./VarelaRound-Regular.ttf', 30)
    max_len = find_max_char_len(string, font)

    _, line_height = font.getsize(string)
    lines = textwrap.wrap(string,width=max_len)

    #Vertically center paragraph
    len_lines = len(lines)
    approx_paragraph_size = len_lines * (line_height + LINE_SPACING)

    h = HEIGHT - topy
    h2 = h / 2
    h3 = h2 - (approx_paragraph_size / 2)

    y_text = topy + h3
    for line in lines:
        size = font.getsize(line)
        draw_obj.text((MARGIN_X, y_text), line, font = font)
        y_text += line_height + LINE_SPACING

def render_title(img,title):
    '''
    Render a title. Returns its bottom y value
    '''

    draw_obj = ImageDraw.Draw(img)
    font = ImageFont.truetype('./VarelaRound-Regular.ttf', 23)
    w,h = font.getsize(title)

    #Figure out how to centre the text
    middle = WIDTH / 2
    half_w = w / 2
    cl = middle - half_w

    # Generate shadow
    shadow='#CCC'
    draw_obj.text((cl+1, MARGIN_Y),title,font=font,fill=shadow)
    draw_obj.text((cl+1, MARGIN_Y+2),title,font=font,fill=shadow)
    draw_obj.text((cl+2, MARGIN_Y+2),title,font=font,fill=shadow)

    # Actual text
    draw_obj.text((cl, MARGIN_Y),title, font = font)
    return h + MARGIN_Y + 5

def render_soon_todo_list(img):
    topy = render_title(img, '@soon Todo List')
    render_tagged_todo_list(img, topy, '@soon')

def render_now_todo_list(img):
    topy = render_title(img, '@now Todo List')
    render_tagged_todo_list(img, topy, '@now')

def render_tagged_todo_list(img, topy, tag):
    items = fetch_todo.fetch_specific_items(tag)
    draw_obj = ImageDraw.Draw(img)
    font = ImageFont.truetype('./DroidSansMono.ttf', 20)
    _, line_height = font.getsize(items[0])
    line_height -= 2 #Adjustment

    reversed_items = reversed(items)

    y_text = topy
    for item in reversed_items:
        clean_item = re.sub(r'^\d{4}-\d{2}-\d{2}', '', item)
        clean_item = clean_item.replace(tag, '')
        clean_item = clean_item.strip()
        clean_item = re.sub(r'\s+', ' ', clean_item)
        clean_item = clean_item.capitalize()
        clean_lines = textwrap.wrap(clean_item,width=48, initial_indent='• ',
                subsequent_indent='  ')
        for line in clean_lines:
            size = font.getsize(line)
            draw_obj.text((MARGIN_X, y_text), line, font = font)
            y_text += line_height
        y_text += 5

def render_random_quote(img):
    draw = ImageDraw.Draw(img)
    quote = fetch_random_quote()
    top = render_title(img, 'Quote:')
    render_paragraph(draw, top, quote)


fns = [render_random_quote, render_now_todo_list, render_soon_todo_list]

def gen_png_byte_stream(png_index):
    img = Image.new('L', (WIDTH, HEIGHT), 'white')

    num_fns = len(fns)
    index_fn = png_index % num_fns
    render_fn = fns[index_fn]

    render_fn(img)
    img_io = BytesIO()
    img.save(img_io, format='png', optimize=True)
    img_io.seek(0)
    content = img_io.getvalue()
    img_io.close()
    return content

if __name__ == "__main__":
    img = Image.new('L', (WIDTH, HEIGHT), 'white')
    render_soon_todo_list(img)
    img.show()


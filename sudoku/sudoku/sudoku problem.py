# In The Name Of God
# Students Name: Rasoul Soltanzadeh - Amirhossein Abyazinejade
# Student ID: 40413160281816 - 
# Teacher Name: Dr. Babagoli
# University: University Of Mazandaran 
# Field Of Study: Computer Engineerung 
# Term: 2
# Course: Discrete Mathematics
# Modify Date:
# Language Version: Python 3.11 (64-bit) 
# Environment: Visiual Studio 2022 Community and
# Subject: Sudoku Problem
# Explainations:
#  این برنامه سودوکو را با منطق گزاره ای حل می کند. بازی سودوکو 4 قانون دارد که عبارنتد از:
#   1- هر خانه یک مقدار دارد از 1 تا 9 دارد
#   2- در هر سطر هر عدد فقط یک بار تکرار می شود
#   3- در هر ستون هر عدد فقط یک بار تکرار می شود
#   4- در هر بلوک سه در سه هر عدد فقط یک باز تکرار می شود
#
#  برای حل سودوکو باید این قوانین را به زبان ریاضیاتی ترجمه کنیم. برای مشاهده منطق ریاضیاتی که
#  برنامه بر اساس آن نوشته شده فایل پی دی اف درون پوشه را باز کنید.
#  مچنین این برنامه توضیحاتی در مورد رضایت بخشی می دهد و اطلاعات CNF Generator را به صورت فایل
#  DIMACS تولید می کند. 


import os
import typing
import pysat as ps
import numpy as np
import pandas as pd
from numpy import array
from pandas import DataFrame
from typing import Iterable
from pysat.formula import CNF
from pysat.solvers import Glucose3


#این متد گزاره P(r, c, v) را به عدادی که نماد این گزاره هستند تبدیل می کند.
def var(r : int, c : int, v : int) -> int:
    return 81*(r-1) + 9*(c-1) + v


# این متد گزاره "هر خانه یکی از اعداد 1 تا 9 را می تواند داشته باشد.
# و فقط یکی از این اعداد را می تواند داشته باشد" را برای هر خانه از جدول سودوکو
# .تولید می کند
def get_cells() -> Iterable:
    # 1) هر خانه حداقل یک مقدار از 1 تا 9 را داشته باشد
    
    logics = []
    for r in range(1, 10):
        for c in range(1, 10):
            logics.append([var(r, c, v) for v in range(1, 10)])

    # 2) هر خانه فقط یک مقدار داشته باشد
    for r in range(1, 10):
        for c in range(1, 10):
            for v in range(1, 10):
                for w in range(v+1, 10):
                    logics.append([-var(r, c, v), -var(r, c, w)])
    return logics


# این متد گزاره "سطر ها می توانند هر کدام از مقادیر 1 تا 9 را اختیار کنند.
# و هر کدام را باید فقط یک بار اختیار کنند" را به ازای هر کدام از سطر ها تولید می کند.
def get_rows() -> Iterable:
    # 1) سطرها : هر کدام از اعداد 1 تا 9 را می توانند اختیار کنند 
    
    logics = []
    for r in range(1, 10):
        for v in range(1, 10):
            logics.append([var(r, c, v) for c in range(1, 10)])

    # 2) سطرها : هر عدد را حداکثر یک بار می توانند اختیار کنند
    for r in range(1, 10):
        for c1 in range(1, 10):
            for c2 in range(c1+1, 10):
                for v in range(1, 10):
                    logics.append([-var(r, c1, v), -var(r, c2, v)])
    return logics


# این متد گزاره " ستون ها می توانند هر کدام از مقادیر 1 تا 9 را اختیار کنند.
# و هر کدام را باید فقط یک بار اختیار کنند" را به ازای هر کدام از ستون ها تولید می کند.
def get_columns() -> Iterable:
    # 1) ستون ها: هر کدام از اعداد 1 تا 9 را می توانند اختیار کنند 
    
    logics = []
    for r in range(1, 10):
        for v in range(1, 10):
            logics.append([var(r, c, v) for c in range(1, 10)])

    # 2) ستون ها: هر عدد را حداکثر یک بار می توانند اختیار کنند
    for c in range(1, 10):
        for r1 in range(1, 10):
            for r2 in range(r1+1, 10):
                for v in range(1, 10):
                    logics.append([-var(r1, c, v), -var(r2, c, v)])
    return logics


# این متد گزاره "بلاک ها می توانند هر کدام از مقادیر 1 تا 9 را اختیار کنند. 
# و هر کدام را باید فقط یک بار اختیار کنند" را به ازای هر کدام از بلاک ها 
# تولید می کند
def get_blocks() -> Iterable:
    # بلاک‌های 3×3
    
    logics = []    
    for br in range(0, 3):
        for bc in range(0, 3):
            for v in range(1, 10):
                cells = []
                for r in range(1 + 3*br, 4 + 3*br):
                    for c in range(1 + 3*bc, 4 + 3*bc):
                        cells.append(var(r, c, v))
                # بلاک ها می توانند هر کدام از مقادیر 1 تا 9 را اختیار کنند
                logics.append(cells)
                # بلاک ها هر کدام از اعدا 1 تا 9 را باید فقط یک بار اختیار کنند 
                for i in range(9):
                    for j in range(i+1, 9):
                        logics.append([-cells[i], -cells[j]])
    return logics


# این متد در واقع هر خانه از سودوکو را به یک گزاره تبدیل می کند. فرق آن با
# get_cells در آن است که get_cells برای هر خانه از سودوکو به ازای هر مقداری
# از 1 تا 9 گزاره تولید می کند. و اما متد get_clueses هر خانه سودوکو را به
# ازای مقداری که کاربر به آن داده به گزاره تبدیل می کند. توجه کنید. مقداری که
# کاربر می دهد می تواند یکی از مقادیر 1 تا 9 یا مقدار خالی باشد. در واقع این
# متد کاری می کند تا گزاره هایی به گزاره های solver اضافه شود. که solver
# خانه های پر را دست نخورده بگذارد. چراکه solver نباید ورودی های کاربر را
# تغییر بدهد. بلکه باید خانه های خالی را پر کند تا جدول سودوکو حل بشود. 
def get_clueses(gird : Iterable) -> Iterable:
    # اضافه کردن clues (اعداد اولیه)
    
    logics = []
    for r in range(1, 10):
        for c in range(1, 10):
            if grid[r-1][c-1] != 0:
                v = grid[r-1][c-1]
                logics.append([var(r, c, v)])
    return logics


# این متد با استفاده از کلاس pysat.formula.CNF() گزاره نرمال فرم CNF را تولید می کند
def sudoku_cnf(grid : Iterable) -> CNF:
    cnf = CNF()
    #قانون اول سودوکو:
    cnf.extend(get_cells())
    #قانون دوم سودوکو برای سطر ها:
    cnf.extend(get_rows())
    #قانون سوم سودوکو برای سطر ها:
    cnf.extend(get_columns())
    #قانون چهارم سودوکو:
    cnf.extend(get_blocks())    
    #قانون پنجم سودوکو:
    cnf.extend(get_clueses(grid))
    return cnf


# این متد با استفاده از کلاس pysat.solvers.Glucose3() سولوری از نوع کلاس Glucose3 .تولید می کند
# به علاوه اگر کاربر جدول سودوکوی اولیه را طوری وارد کرده باشد که هیچ جواب قابل قبولی برای آن
# وجود نداشته باشد. این متد None, None, CNF خروجی می دهد
def solve_sudoku(grid : Iterable) -> tuple[Iterable, Iterable, CNF] | tuple[None, None, CNF]:
    cnf = sudoku_cnf(grid)
    solver = Glucose3()
    solver.append_formula(cnf.clauses)
    
    if solver.solve():
        model = solver.get_model()
        
        # پاسخ را به جدول 9×9 تبدیل می‌کنیم
        solution = [[0]*9 for _ in range(9)]
        
        for r in range(1, 10):
            for c in range(1, 10):
                for v in range(1, 10):
                    if var(r, c, v) in model:
                        solution[r-1][c-1] = v

        return solution, model, cnf
    else: return None, None, cnf


#
def save_cnf(path : str, cnf : CNF) -> str: 
    try:
        cnf.to_file(path)
        return "File save shod."
    except: return "File save nashod. Dar masir file moshkeli vojod darad."


# grid برد 9*9 سودوکواست و عدد صفر در آن نماد خانه خالی است که solver باید آن را پر کند.
grid = [
    [1,0,0, 0,0,0, 0,0,0],
    [0,2,0, 0,0,0, 0,0,0],
    [0,0,3, 0,0,0, 0,0,0],

    [0,0,0, 4,0,0, 0,0,0],
    [0,0,0, 0,5,0, 0,0,0],
    [0,0,0, 0,0,6, 0,0,0],

    [0,0,0, 0,0,0, 7,0,0],
    [0,0,0, 0,0,0, 0,8,0],
    [0,0,0, 0,0,0, 0,0,9],
] # به جای این آرایه باید برنامه ای نوشته بشود که از کاربر جدول سودوکو 9*9 را دریافت کند
# و آن را مثل آرایه بالا برگرداند

# برنامه اصلی
# در برنامه اصلی  grid از کاربر ورودی گرفته شود. و متغییر های دیگری که در پایین توضیحات
#  آنان نوشته شده اند به عنوان جواب برنامه چاپ بشود. اگر solve_sudoku خروجی به شکل None, None, CNF داد طبق توضیحات
#  این متد. هیچ جواب قابل قبولی برای جدول وجود ندارد. یعنی کاربر جدول را با آرایش غلطی از اعداد وارد کرده
#  که قوانین سودوکو را به هم زده اند. و از کاربر پرسیده شود آیا می خواهید CNF Generator را به شکل فایل .DIMACS 
# دریافت کنید. در صورت پاسخ مثبت با استفاده از متد save_cnf این کار انجام شود. و باید مسیری که کاربر می خواهد فایل در آن سیو شود 
#  را از کاربر گرفت و فایل را در آن آپلود کرد. یا می توان مسیر پروژه را با کمک کتابخانه os دریافت و در آن آپلود کرد. به علاوه بهتر است 
# در مکان هایی که از کاربر ورودی می گیریم مکانیزیمی در نظر گرفته شود تا ورودی های نا معتبر را از گاربر قبول نکند. همچنین بهتر است 
# تمام توضیحات درون پروژه و متد ها خوانده شوند. برای دخل تصرف در کد ها محدودیتی وجود ندارد.
satisfiability_txt = (
        + "\n  Tozih dar mored satisfiability:\n"
        + "Yani dar ebarati az gozaarehaye manteghi halati vojud dashte bashad ke tamam gozaareha ra erza konad."
        + " Yani ham gozaarehaye mosbat va ham gozaarehaye manfi arzesh True peyda konand.\n"
)# این متن باید در برنامه چاپ بشود
more_info_txt = (
        "\n   Etelaate bishtar:\n"
        + "Dar in barname az ketabkhane pysat estefade shode ast. Va az solver az noe pysat."
        + "solvers.Glucose3() estefade shode va az CNF Generator az noe pysat.formula.CNF() estefade shode ast.\n\n"
)# این متن باید در برنامه چاپ بشود
solution, model, cnf = solve_sudoku(grid) 
model = array(model) #model که باید چاپ بشود
solution = array(solution) #جدول سودوکو حل شده باید چاپ بشود
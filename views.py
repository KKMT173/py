import qrcode
import os
from django.shortcuts import render, redirect
from django.template import loader
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse,JsonResponse
from django.db import connection,IntegrityError
from django import template

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_login WHERE username = %s AND password = %s", [username, password])
            user_data = cursor.fetchone()
        if user_data is not None:
            # การยืนยันสำเร็จ ดำเนินการตามที่ต้องการ เช่น เก็บข้อมูลผู้ใช้งานใน session และเปลี่ยนเส้นทางไปยังหน้าหลังเข้าสู่ระบบ
            request.session['id_user_type'] = user_data[3]
            request.session['username'] = user_data[1]# เก็บค่า id_user_type ใน session
            return redirect('WebsmartunityQR')
        else:
            error_message = 'กรุณาตรวจสอบ Username เเละ Password ให้ถูกต้อง'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def WebsmartunityQR(request):
    # เช็คว่าผู้ใช้เข้าสู่ระบบแล้วหรือไม่ หากยังไม่ได้เข้าสู่ระบบให้เปลี่ยนเป็นการ redirect ไปหน้าเข้าสู่ระบบ
    # if not request.user.is_authenticated:
    #     return redirect('login')  # ให้เปลี่ยนเป็นชื่อ URL pattern ของหน้า login ที่คุณต้องการ
    template = loader.get_template('master.html')
    context = {
        # 'firstname': 'mintorn',
        # 'nickname': 'KK',
        'username': request.session['username']
    }
    return HttpResponse(template.render(context, request))

def add_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type_id = request.POST['user_type']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_login (username, password, id_user_type) VALUES (%s, %s, %s)",
                           [username, password, user_type_id])
        return redirect('userlist')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_type")
        user_types = cursor.fetchall()
    return render(request, 'adduser.html', {'user_types': user_types})

def user_list_view(request):
    # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
    with connection.cursor() as cursor:
        cursor.execute("select * from user_login left outer join user_type on user_login.id_user_type = user_type.id ")
        user_data = cursor.fetchall()
        print(user_data)
    return render(request, 'userlist.html', {'users': user_data})

def edit_user_view(request, user_id):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type_id = request.POST['user_type']
        # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและแก้ไขข้อมูลผู้ใช้งาน
        with connection.cursor() as cursor:
            cursor.execute("UPDATE user_login SET username = %s, password = %s, id_user_type = %s WHERE id = %s",
                           [username, password, user_type_id,user_id])
        # ดำเนินการตามที่ต้องการ เช่น เปลี่ยนเส้นทางไปยังหน้าแสดงรายการผู้ใช้งาน
        return redirect('userlist')
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_type")
            user_types = cursor.fetchall()
    # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งานที่ต้องการแก้ไข
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_login WHERE id = %s", [user_id])
        user_data = cursor.fetchone()
    return render(request, 'useredit.html', {'user': user_data , 'user_types': user_types})

def userdelete(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_login WHERE id = %s", [user_id])
    return redirect('userlist')

# def GenQr(request):
#     template = loader.get_template('genqr.html')
#     return HttpResponse(template.render())

# def checklist_view(request):
#     if request.method == 'POST':
#         # ดึงรายการเช็คลิสต์ที่ถูกเลือกมาจาก request.POST
#         selected_items = [key for key in request.POST if key.startswith('checklist_item_')]
#         # ดึงค่าของแต่ละรายการที่ถูกเลือก
#         checked_items = [request.POST[key] for key in selected_items]
#
#     checklist_items = ['Item 1', 'Item 2', 'Item 3']  # รายการเช็คลิสต์
#
#     return render(request, 'checklist.html', {'checklist_items': checklist_items})

def generate_qr_code(request):
    if request.method == 'POST':
        area = request.POST.get('area', '')
        id_department = request.POST.get('department', '')
        id_ch_li_type = request.POST.get('check_list_type', '')
        selected_checkboxes = request.POST.getlist('checklist_item')

        # Combine item_code and id_department into a single string
        data = f"{area}, {id_department}, {id_ch_li_type} "
        data += ", ".join(selected_checkboxes)

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        # Save the QR code image to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_image = buffer.getvalue()

        # Save data to PostgreSQL

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO unity_check_list (id_area, id_department, qr_code, id_ch_list_type, remark) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id",
                    [area, id_department, data, id_ch_li_type, ", ".join(selected_checkboxes)]
                )
                unity_check_list_id = cursor.fetchone()[0]  # ดึงค่า id ที่ถูกเพิ่มล่าสุด
                # เพิ่มข้อมูลลงในตาราง unity_check_list_detail
                for checkbox in selected_checkboxes:
                    cursor.execute(
                        "INSERT INTO unity_check_list_detail (id_un_ch_list, check_list) VALUES (%s, %s)",
                        [unity_check_list_id, checkbox]
                    )
            except Exception as e:
                print("Error inserting data:", e)

        # Save the QR code image to the desired location
        qr_code_filename = f"{data}.png"
        qr_code_path = os.path.join("qrcodes", qr_code_filename)
        full_qr_code_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)
        with open(full_qr_code_path, "wb") as f:
            f.write(qr_code_image)

        # Print for debugging
        print(data)
        print(qr_code_path)
        print(full_qr_code_path)

        # Return the rendered HTML with the QR code image path
        return render(request, 'genqr.html', {'qr_code_path': qr_code_path, 'areas': get_areas(), 'departments': get_departments(), 'check_list_types': get_unity_check_list_type(),})
    else:
        return render(request, 'genqr.html', {'areas': get_areas(), 'departments': get_departments(), 'check_list_types': get_unity_check_list_type()})

# สมมติว่า check_list_type_id เป็นชนิดข้อมูลแบบ int หรือตัวเลข
def get_checkboxes(request, check_list_type_id):
    with connection.cursor() as cursor:
        if check_list_type_id == 1:
            cursor.execute(
                # Query สำหรับเมื่อ check_list_type_id เป็น 1
                "SELECT unity_check_list_type.id, unity_check_list_type.name_ch_type, unity_item.unity_name, unity_item_detail.detail_name, unity_sub_item.un_sub_num, unity_item.id, unity_item_detail.id FROM unity_check_list_type LEFT OUTER JOIN unity_item ON unity_check_list_type.id = unity_item.unity_item_type LEFT OUTER JOIN unity_item_detail ON unity_item.id = unity_item_detail.id_unity_item LEFT OUTER JOIN unity_sub_item ON unity_item_detail.id = unity_sub_item.id_un_item_detail WHERE unity_check_list_type.id = %s order by unity_check_list_type.id,unity_item.id,unity_item_detail.id",
                [check_list_type_id]
            )
            rows = cursor.fetchall()

            checkboxes = []
            for row in rows:
                un_sub_num_list = row[4].split(",") if row[4] else []
                headvalue = f"{row[0]}-{row[5]}"
                value = f"{row[0]}-{row[5]}-{row[6]}"  # รวมค่า unity_item.id และ unity_item_detail.id เข้าด้วยกันด้วยเครื่องหมายขีดกลาง (-)
                checkbox = {
                    'id': row[0],
                    'unity_name': row[2],  # เป็นหัวข้อใหญ่
                    'detail_name': row[3],  # เป็นหัวข้อย่อย 1.1
                    'un_sub_num': un_sub_num_list,  # เป็น list ของหัวข้อย่อยของ 'detail_name': row[3]
                    'item_id': value,
                    'un_item_id': headvalue,
                }
                checkboxes.append(checkbox)

        else:
            cursor.execute(
                # Query สำหรับเมื่อ check_list_type_id ไม่ใช่ 1
                "SELECT unity_check_list_type.id, unity_check_list_type.name_ch_type, unity_item.unity_name, unity_item_detail.detail_name, unity_item.id as item_id2, unity_item_detail.id FROM unity_check_list_type left outer join unity_item on unity_check_list_type.id = unity_item.unity_item_type left outer join unity_item_detail on unity_item.id = unity_item_detail.id_unity_item WHERE unity_check_list_type.id = %s order by unity_check_list_type.id,unity_item.id,unity_item_detail.id",
                [check_list_type_id]
            )
            rows = cursor.fetchall()

            checkboxes = []
            for row in rows:
                headvalue = f"{row[0]}-{row[4]}"
                checkbox = {
                    'id': row[0],
                    'unity_name': row[2],  # เป็นหัวข้อใหญ่
                    'detail_name': row[3],  # เป็นหัวข้อย่อย 1.1
                    'item_id2': headvalue,  # เพิ่มตัวแปร item_id2 เก็บค่า unity_item.id
                }
                checkboxes.append(checkbox)

    return JsonResponse(checkboxes, safe=False)

def get_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM department where id <> 36")
        departments = []
        for row in cursor.fetchall():
            department = {
                'id': row[0],
                'name': row[1]
            }
            departments.append(department)
    return departments

def get_areas():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM area ")
        areas = []
        for row in cursor.fetchall():
            area = {
                'id': row[0],
                'name': row[1]
            }
            areas.append(area)
    return areas

def get_unity_check_list_type():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM unity_check_list_type ")
        check_list_types = []
        for row in cursor.fetchall():
            check_list_type = {
                'id_ch_li_type': row[0],
                'name_ch_li_type': row[1]
            }
            check_list_types.append(check_list_type)
    return check_list_types

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('/login')

import qrcode
import hashlib
import os
from django.shortcuts import render, redirect
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse,JsonResponse
from django.db import connection,IntegrityError,connections
from django.urls import reverse




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        md5_password = hashlib.md5(password.encode()).hexdigest().upper()

        # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
        with connections['default'].cursor() as cursor:
            # ดึงข้อมูลผู้ใช้จากตาราง user_login
            cursor.execute("SELECT * FROM user_login WHERE username = %s", [username])
            user_login_data = cursor.fetchone()

            if user_login_data is not None:
                # หากมีผู้ใช้งานในตาราง user_login
                # เช็ครหัสผ่านจากตาราง user_list
                with connections['user_list'].cursor() as cursor_user_list:
                    cursor_user_list.execute("SELECT * FROM user_list ul WHERE ul.id = %s AND ul.password = %s",
                                             [username, md5_password])
                    user_data = cursor_user_list.fetchone()

                    if user_data is not None:
                        # การยืนยันสำเร็จ ดำเนินการตามที่ต้องการ เช่น เก็บข้อมูลผู้ใช้งานใน session และเปลี่ยนเส้นทางไปยังหน้าหลังเข้าสู่ระบบ
                        request.session['id_user_type'] = user_login_data[3]
                        request.session['username'] = user_data[0]
                        request.session['department'] = user_data[6]
                        return redirect('WebsmartunityQR')
                    else:
                        error_message = 'รหัสผ่านไม่ถูกต้อง'
            else:
                error_message = 'Username ไม่ถูกต้อง'

            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         md5_password = hashlib.md5(password.encode()).hexdigest()
#         # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM user_login WHERE username = %s AND password = %s", [username, password])
#             user_data = cursor.fetchone()
#         if user_data is not None:
#             # การยืนยันสำเร็จ ดำเนินการตามที่ต้องการ เช่น เก็บข้อมูลผู้ใช้งานใน session และเปลี่ยนเส้นทางไปยังหน้าหลังเข้าสู่ระบบ
#             request.session['id_user_type'] = user_data[3]
#             request.session['username'] = user_data[1]# เก็บค่า id_user_type ใน session
#             return redirect('WebsmartunityQR')
#         else:
#             error_message = 'กรุณาตรวจสอบ Username เเละ Password ให้ถูกต้อง'
#             return render(request, 'login.html', {'error_message': error_message})
#     return render(request, 'login.html')

# def WebsmartunityQR(request):
# #     # เช็คว่าผู้ใช้เข้าสู่ระบบแล้วหรือไม่ หากยังไม่ได้เข้าสู่ระบบให้เปลี่ยนเป็นการ redirect ไปหน้าเข้าสู่ระบบ
# #     # if not request.user.is_authenticated:
# #     #     return redirect('login')  # ให้เปลี่ยนเป็นชื่อ URL pattern ของหน้า login ที่คุณต้องการ
# #     template = loader.get_template('master.html')
# #     context = {
# #         # 'firstname': 'mintorn',
# #         # 'nickname': 'KK',
# #         'username': request.session['username']
# #     }
# #     return HttpResponse(template.render(context, request))

# def WebsmartunityQR(request):
#     # Execute SQL queries to get data
#     with connection.cursor() as cursor:
#         cursor.execute("""select distinct
#                                 (SELECT COUNT(*)
#                                  FROM unity_check_list
#                                  WHERE
#                                     status = 3
#                                     AND id_ch_list_type = 1
#                                     AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                  ),
#                                 (SELECT COUNT(*)
#                                  FROM unity_check_list
#                                  WHERE
#                                     status <> 3
#                                     AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                     AND id_ch_list_type = 1
#                                  ),
#                                 (SELECT COUNT(*)
#                                 FROM unity_check_list
#                                 WHERE
#                                     EXTRACT(MONTH FROM refdate)< EXTRACT(MONTH FROM CURRENT_DATE)
#                                     AND id_ch_list_type = 1
#                                 )
#                             from
#                             unity_check_list""")
#         data1 = cursor.fetchone()
#         cursor.execute("""select distinct
#                                 (SELECT COUNT(*)
#                                  FROM unity_check_list
#                                  WHERE
#                                     status = 3
#                                     AND id_ch_list_type = 2
#                                     AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                  ),
#                                 (SELECT COUNT(*)
#                                  FROM unity_check_list
#                                  WHERE
#                                     status <> 3
#                                     AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                     AND id_ch_list_type = 2
#                                  ),
#                                 (SELECT COUNT(*)
#                                 FROM unity_check_list
#                                 WHERE
#                                     EXTRACT(MONTH FROM refdate)< EXTRACT(MONTH FROM CURRENT_DATE)
#                                     AND id_ch_list_type = 2
#                                 )
#                             from
#                             unity_check_list""")
#         data2 = cursor.fetchone()
#         cursor.execute("""select distinct
#                             (SELECT COUNT(*)
#                              FROM unity_check_list
#                              WHERE
#                                 status = 3
#                                 AND id_ch_list_type = 3
#                                 AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                              ),
#                             (SELECT COUNT(*)
#                              FROM unity_check_list
#                              WHERE
#                                 status <> 3
#                                 AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                 AND id_ch_list_type = 3
#                              ),
#                             (SELECT COUNT(*)
#                             FROM unity_check_list
#                             WHERE
#                                 EXTRACT(MONTH FROM refdate)< EXTRACT(MONTH FROM CURRENT_DATE)
#                                 AND id_ch_list_type = 3
#                             )
#                         from
#                         unity_check_list
#                         """)
#         data3 = cursor.fetchone()
#         cursor.execute("""select distinct
#                             (SELECT COUNT(*)
#                              FROM unity_check_list
#                              WHERE
#                                 status = 3
#                                 AND id_ch_list_type = 4
#                                 AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                              ),
#                             (SELECT COUNT(*)
#                              FROM unity_check_list
#                              WHERE
#                                 status <> 3
#                                 AND EXTRACT(MONTH FROM refdate)=EXTRACT(MONTH FROM CURRENT_DATE)
#                                 AND id_ch_list_type = 4
#                             ),
#                             (SELECT COUNT(*)
#                             FROM unity_check_list
#                             WHERE
#                                 EXTRACT(MONTH FROM refdate)< EXTRACT(MONTH FROM CURRENT_DATE)
#                                 AND id_ch_list_type = 4
#                             )
#                         from
#                         unity_check_list""")
#         data4 = cursor.fetchone()
#
#     # Prepare data for rendering in JavaScript
#     pie_chart_data = [
#         {"green": data1[0], "yellow": data1[1], "red": data1[2]},
#         {"green": data2[0], "yellow": data2[1], "red": data2[2]},
#         {"green": data3[0], "yellow": data3[1], "red": data3[2]},
#         {"green": data4[0], "yellow": data4[1], "red": data4[2]},
#     ]
#
#     context = {
#         'pie_chart_data': json.dumps(pie_chart_data),
#         'username': request.session['username']
#     }
#
#     return render(request, 'master.html', context)

def WebsmartunityQR(request):
    if 'username' not in request.session:
        return redirect('login')
    with connection.cursor() as cursor:
        cursor.execute(
            """ select unity_check_list.id,department.department_name,area.area_name,unity_check_list_type.name_ch_type,date(unity_check_list.refdate),
                unity_check_list.status,
                (SELECT
                    CASE
                        WHEN unity_check_list.status = 4 THEN  'Approved'
                        WHEN unity_check_list.status = 3 THEN  'Waiting Approved'
                        WHEN unity_check_list.status = 2 THEN  'Waiting Checked'
                        WHEN unity_check_list.status = 1 THEN  'Waiting Inspected'
                        ELSE NULL 
                    END AS name_status),
                (SELECT
                    CASE
                        WHEN unity_check_list.status = 4  AND EXTRACT(MONTH FROM unity_check_list.refdate)=EXTRACT(MONTH FROM CURRENT_DATE)  THEN 'g'
                        WHEN unity_check_list.status <> 4 AND EXTRACT(MONTH FROM unity_check_list.refdate)=EXTRACT(MONTH FROM CURRENT_DATE)  THEN 'y'
                        WHEN EXTRACT(MONTH FROM unity_check_list.refdate)< EXTRACT(MONTH FROM CURRENT_DATE) THEN 'r'
                        ELSE NULL 
                    END AS colour)
                from unity_check_list 
                left outer join department on unity_check_list.id_department = department.id 
                left outer join area on unity_check_list.id_area = area.id 
                left outer join  unity_check_list_type on unity_check_list.id_ch_list_type = unity_check_list_type.id 
            """)
        check_list_data = cursor.fetchall()
        # print(check_list_data)
    # context = {
    #     'username': request.session['username']
    # }

    return render(request, 'master.html',{'listchecklists': check_list_data})

# def add_user(request):
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user_type_id = request.POST['user_type']
#         with connection.cursor() as cursor:
#             cursor.execute("INSERT INTO user_login (username, password, id_user_type) VALUES (%s, %s, %s)",
#                            [username, password, user_type_id])
#         return redirect('userlist')
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM user_type")
#         user_types = cursor.fetchall()
#     return render(request, 'adduser.html', {'user_types': user_types})

def add_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        user_type_id = request.POST['user_type']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_login (username, id_user_type) VALUES (%s, %s)",
                           [username, user_type_id])
        return redirect('userlist')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_type")
        user_types = cursor.fetchall()
    return render(request, 'adduser.html', {'user_types': user_types})

def user_list_view(request):
    # เชื่อมต่อกับฐานข้อมูล user_login และดึงข้อมูลผู้ใช้
    with connections['default'].cursor() as cursor_user_login:
        cursor_user_login.execute("""
           select ulo.id, ulo.username, ut.name_user_type 
           from user_login ulo 
           left outer join user_type ut  on ulo.id_user_type = ut.id
        """)
        user_login_data = cursor_user_login.fetchall()

    # เชื่อมต่อกับฐานข้อมูล user_list และดึงข้อมูลผู้ใช้
    with connections['user_list'].cursor() as cursor_user_list:
        cursor_user_list.execute("""
            SELECT ul.id, ul.password, ul.user_index, dc.department_name, sc.section_name, pc.position_name, 
                   gc.group_name, us.status_name, ul.name_th, concat(ul.firstname, ' ', ul.surname) as full_name, ul.department_index
            FROM user_list AS ul
            LEFT OUTER JOIN department_control AS dc ON ul.department_index = dc.department_index
            LEFT OUTER JOIN section_control AS sc ON ul.section_index = sc.section_index
            LEFT OUTER JOIN position_control AS pc ON ul.position_index = pc.position_index
            LEFT OUTER JOIN group_control AS gc ON ul.group_index = gc.group_index
            LEFT OUTER JOIN user_status AS us ON ul.status_index = us.status_index
            WHERE ul.status_index = 1 AND ul.department_index = %s
        """, [request.session['department']])
        user_list_data = cursor_user_list.fetchall()
    # สร้างรายการแบบดิกชันารีของข้อมูลผู้ใช้จาก user_login

    # รวมข้อมูลจากทั้งสองแหล่ง
    combined_data = []
    for user_login_row in user_login_data:
        for user_list_row in user_list_data:
            if user_login_row[1] == user_list_row[0]:
                combined_data.append({
                    'id': user_login_row[0],
                    'username': user_login_row[1],
                    'user_type': user_login_row[2],
                    'user_index': user_list_row[2],
                    'department_name': user_list_row[3],
                    'section_name': user_list_row[4],
                    'position_name': user_list_row[5],
                    'group_name': user_list_row[6],
                    'status_name': user_list_row[7],
                    'name_th': user_list_row[8],
                    'full_name': user_list_row[9]
                })
    # print(user_login_data)
    # print(user_list_data)
    # ส่งข้อมูลไปยังเทมเพลตสำหรับการแสดงผล
    return render(request, 'userlist.html', {'users': combined_data})

# def user_list_view(request):
#     # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
#     with connections['default'].cursor() as cursor_user_login:
#         cursor_user_login.execute("select ul.id,ul.username,ut.name_user_type from user_login ul left outer join user_type ut  on ul.id_user_type = ut.id")
#         user_login_data = cursor_user_login.fetchall()
#
#     # เชื่อมต่อกับฐานข้อมูล user_list
#     with connections['user_list'].cursor() as cursor_user_list:
#         cursor_user_list.execute("""
#             SELECT ul.id, ul.password, ul.user_index, dc.department_name, sc.section_name, pc.position_name,
#                    gc.group_name, us.status_name, ul.name_th, concat(ul.firstname, ' ', ul.surname) as full_name
#             FROM user_list AS ul
#             LEFT OUTER JOIN department_control AS dc ON ul.department_index = dc.department_index
#             LEFT OUTER JOIN section_control AS sc ON ul.section_index = sc.section_index
#             LEFT OUTER JOIN position_control AS pc ON ul.position_index = pc.position_index
#             LEFT OUTER JOIN group_control AS gc ON ul.group_index = gc.group_index
#             LEFT OUTER JOIN user_status AS us ON ul.status_index = us.status_index
#             WHERE ul.status_index = 1
#         """)
#         user_list_data = cursor_user_list.fetchall()
#
#     # ทำการรวมข้อมูลจาก user_login และ user_list ตามความเหมาะสม
#     combined_data = []
#     for user_login_row in user_login_data:
#         for user_list_row in user_list_data:
#             if user_login_row[0] == user_list_row[0]:
#                 combined_data.append({
#                     'username': user_login_row[1],
#                     'user_type': user_list_row[2],
#                     # เพิ่มข้อมูลอื่น ๆ ตามต้องการ
#                 })
#
#     # ส่งข้อมูลไปยังเทมเพลตสำหรับการแสดงผล
#     return render(request, 'userlist.html', {'users': combined_data})


def edit_user_view(request, user_id):
    if request.method == 'POST':
        username = request.POST['username']
        # password = request.POST['password']
        user_type_id = request.POST['user_type']
        # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและแก้ไขข้อมูลผู้ใช้งาน
        with connection.cursor() as cursor:
            cursor.execute("UPDATE user_login SET username = %s, id_user_type = %s WHERE id = %s",
                           [username, user_type_id,user_id])
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

# def generate_qr_code(request):
#     if request.method == 'POST':
#         area = request.POST.get('area', '')
#         id_department = request.POST.get('department', '')
#         id_ch_li_type = request.POST.get('check_list_type', '')
#         selected_checkboxes = request.POST.getlist('checklist_item')
#
#         # Combine item_code and id_department into a single string
#         data = f"{area}, {id_department}, {id_ch_li_type} "
#         # data += ", ".join(selected_checkboxes)
#
#         # Generate QR code
#         qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#         qr.add_data(data)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color='black', back_color='white')
#
#         # Save the QR code image to a BytesIO object
#         buffer = BytesIO()
#         img.save(buffer, format='PNG')
#         qr_code_image = buffer.getvalue()
#
#         # Save data to PostgreSQL
#
#         try:
#             with connection.cursor() as cursor:
#                 # Check for duplicate entry before inserting
#                 cursor.execute(
#                     "SELECT id FROM unity_check_list WHERE id_area = %s AND id_department = %s AND id_ch_list_type = %s",
#                     [area, id_department, id_ch_li_type]
#                 )
#                 duplicate_entry = cursor.fetchone()
#
#                 if duplicate_entry:
#                     return render(request, 'genqr.html',
#                                   {'duplicate_error': True, 'areas': get_areas(), 'departments': get_departments(),
#                                    'check_list_types': get_unity_check_list_type()})
#
#                 # No duplicate entry, proceed with insertion
#                 cursor.execute(
#                     "INSERT INTO unity_check_list (id_area, id_department, qr_code, id_ch_list_type, remark) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id",
#                     [area, id_department, data, id_ch_li_type, ", ".join(selected_checkboxes)]
#                 )
#                 unity_check_list_id = cursor.fetchone()[0]  # ดึงค่า id ที่ถูกเพิ่มล่าสุด
#                 # เพิ่มข้อมูลลงในตาราง unity_check_list_detail
#                 for checkbox in selected_checkboxes:
#                     cursor.execute(
#                         "INSERT INTO unity_check_list_detail (id_un_ch_list, check_list) VALUES (%s, %s)",
#                         [unity_check_list_id, checkbox]
#                     )
#         except IntegrityError as e:
#             return render(request, 'genqr.html',
#                           {'duplicate_error': True, 'areas': get_areas(), 'departments': get_departments(),
#                            'check_list_types': get_unity_check_list_type()})
#         except Exception as e:
#             print("Error inserting data:", e)
#
#         # Save the QR code image to the desired location
#         qr_code_filename = f"{data}.png"
#         qr_code_path = os.path.join("qrcodes", qr_code_filename)
#         full_qr_code_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)
#         with open(full_qr_code_path, "wb") as f:
#             f.write(qr_code_image)
#
#         # Print for debugging
#         print(data)
#         print(qr_code_path)
#         print(full_qr_code_path)
#
#         # Return the rendered HTML with the QR code image path
#         return render(request, 'genqr.html', {'qr_code_path': qr_code_path, 'areas': get_areas(), 'departments': get_departments(), 'check_list_types': get_unity_check_list_type(),})
#     else:
#         return render(request, 'genqr.html', {'areas': get_areas(), 'departments': get_departments(), 'check_list_types': get_unity_check_list_type()})
#

def generate_qr_code(request):
    if request.method == 'POST':
        area = request.POST.get('area', '')
        id_department = request.POST.get('department', '')
        id_ch_li_type = request.POST.get('check_list_type', '')
        selected_checkboxes = request.POST.getlist('checklist_item')
        data = f"{area}, {id_department}, {id_ch_li_type}, "
        data += ", ".join(selected_checkboxes)
        textbox_item3 = request.POST.get('textbox_item3', '')
        textbox_item4 = request.POST.get('textbox_item4', '')
        textbox_item5 = request.POST.get('textbox_item5', '')
        textbox_item44 = request.POST.get('textbox_item44', '')
        item_code = f"{textbox_item3}!{textbox_item4}!{textbox_item5}!{textbox_item44}"
        # รวมข้อมูลจาก textbox กับข้อมูล checkboxes
        data += f"{textbox_item3}!{textbox_item4}!{textbox_item5}!{textbox_item44}"
        # รวมข้อมูลจาก textbox ด้วยข้อมูล checkboxes
        # Save data to PostgreSQL

        try:
            with connection.cursor() as cursor:
                # Check for duplicate entry before inserting
                cursor.execute(
                    "SELECT id FROM unity_check_list WHERE id_area = %s AND id_department = %s AND id_ch_list_type = %s",
                    [area, id_department, id_ch_li_type]
                )
                duplicate_entry = cursor.fetchone()

                if duplicate_entry:
                    return render(request, 'genqr.html',
                                  {'duplicate_error': True, 'areas': get_areas(), 'departments': get_departments(), 'check_list_types': get_unity_check_list_type()})
                # No duplicate entry, proceed with insertion
                cursor.execute(
                    "INSERT INTO unity_check_list (id_area, id_department, id_ch_list_type, remark, data,itemcode,status) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id",
                    [area, id_department, id_ch_li_type,", ".join(selected_checkboxes),data,item_code,1]
                )
                # unity_check_list_id = cursor.fetchone()[0]  # Get the inserted ID
                unity_check_list_id = cursor.fetchone()[0]


                for checkbox in selected_checkboxes:
                    cursor.execute(  "INSERT INTO unity_check_list_detail (id_un_ch_list, check_list) VALUES (%s, %s)",
                                            [unity_check_list_id, checkbox]
                                        )
                # Set the data variable with unity_check_list_id
                base_url = request.build_absolute_uri('/')
                # data = f"{unity_check_list_id}"
                data = f"{base_url}M_checklist_report/{unity_check_list_id}/"  # URL ของหน้า "Checklist report"
                print(unity_check_list_id)

                # Generate QR code
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')

                # Save the QR code image to a BytesIO object
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                qr_code_image = buffer.getvalue()

                # Save the QR code image to the desired location
                qr_code_filename = f"{unity_check_list_id}.png"
                qr_code_path = os.path.join("qrcodes", qr_code_filename)
                full_qr_code_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)
                with open(full_qr_code_path, "wb") as f:
                    f.write(qr_code_image)

                # Generate the URL for the "Checklist report" using the reverse function
                report_url = reverse('checklist_report', args=[unity_check_list_id])
                # Redirect to the "Checklist report" page after successfully generating QR code
                return redirect(report_url)

        except IntegrityError as e:
            return render(request, 'genqr.html',
                          {'duplicate_error': True, 'areas': get_areas(), 'departments': get_departments(),
                           'check_list_types': get_unity_check_list_type()})
        except Exception as e:
            print("Error inserting data:", e)

    else:
        return render(request, 'genqr.html', {'areas': get_areas(), 'departments': get_departments(),'check_list_types': get_unity_check_list_type(),'userlists' : get_userlist(request) })

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
                headvalue = f"{row[0]}!{row[5]}"
                value = f"{row[0]}!{row[5]}!{row[6]}"  # รวมค่า unity_item.id และ unity_item_detail.id เข้าด้วยกันด้วยเครื่องหมายขีดกลาง (-)
                checkbox = {
                    'id': row[0],
                    'unity_name': row[2],  # เป็นหัวข้อใหญ่
                    'detail_name': row[3],  # เป็นหัวข้อย่อย 1.1
                    'un_sub_num': un_sub_num_list,  # เป็น list ของหัวข้อย่อยของ 'detail_name': row[3]
                    'item_id': value,
                    'un_item_id': headvalue,
                }
                checkboxes.append(checkbox)

        elif check_list_type_id == 2:
            cursor.execute(
                # Query สำหรับเมื่อ check_list_type_id ไม่ใช่ 1
                "SELECT unity_check_list_type.id, unity_check_list_type.name_ch_type, unity_item.unity_name, unity_item_detail.detail_name, unity_item.id as item_id2, unity_item_detail.id FROM unity_check_list_type left outer join unity_item on unity_check_list_type.id = unity_item.unity_item_type left outer join unity_item_detail on unity_item.id = unity_item_detail.id_unity_item WHERE unity_check_list_type.id = %s order by unity_check_list_type.id,unity_item.id,unity_item_detail.id",
                [check_list_type_id]
            )
            rows = cursor.fetchall()

            checkboxes = []
            for row in rows:
                headvalue = f"{row[0]}!{row[4]}"
                checkbox = {
                    'id': row[0],
                    'unity_name': row[2],  # เป็นหัวข้อใหญ่
                    'detail_name': row[3],  # เป็นหัวข้อย่อย 1.1
                    'item_id2': headvalue,  # เพิ่มตัวแปร item_id2 เก็บค่า unity_item.id
                }
                checkboxes.append(checkbox)
        elif check_list_type_id == 4:
            cursor.execute(
                # Query สำหรับเมื่อ check_list_type_id ไม่ใช่ 1
                """SELECT unity_check_list_type.id, unity_check_list_type.name_ch_type, unity_item.unity_name,
                unity_item_detail.detail_name, unity_item.id as item_id2, unity_item_detail.id 
                FROM unity_check_list_type 
                left outer join unity_item on unity_check_list_type.id = unity_item.unity_item_type 
                left outer join unity_item_detail on unity_item.id = unity_item_detail.id_unity_item 
                WHERE unity_check_list_type.id = 4 order by unity_check_list_type.id,unity_item.id,unity_item_detail.id""",
                [check_list_type_id]
            )
            rows = cursor.fetchall()

            checkboxes = []
            for row in rows:
                headvalue = f"{row[0]}!{row[4]}"
                checkbox = {
                    'id': row[0],
                    'unity_name': row[2],  # เป็นหัวข้อใหญ่
                    'detail_name': row[3],  # เป็นหัวข้อย่อย 1.1
                    'item_id2': headvalue,  # เพิ่มตัวแปร item_id2 เก็บค่า unity_item.id
                }
                checkboxes.append(checkbox)
    return JsonResponse(checkboxes, safe=False)

def get_userlist(request):
    # เช็ครหัสผ่านจากตาราง user_list
                with connections['user_list'].cursor() as cursor_user_list:
                    cursor_user_list.execute("""select concat(ul.firstname, ' ', ul.surname) as full_name,* 
                                                from user_list ul where department_index = %s and status_index = 1"""
                                             ,[request.session['department']])
                    userlists = cursor_user_list.fetchall()
                return userlists

# def get_departments():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM department where id <> 36")
#         departments = []
#         for row in cursor.fetchall():
#             department = {
#                 'id': row[0],
#                 'name': row[1]
#             }
#             departments.append(department)
#     return departments

def get_departments():
    with connections['user_list'].cursor() as cursor_user_list:
        cursor_user_list.execute("select * from department_control where department_index <> 36")
        departments = []
        for row in cursor_user_list.fetchall():
            department = {
                'id': row[1],
                'name': row[0]
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

# def get_areas_by_department(request, department_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM area WHERE id_department = %s", [department_id])
#         areas = []
#         for row in cursor.fetchall():
#             area = {
#                 'id': row[0],
#                 'name': row[1]
#             }
#             areas.append(area)
#     return JsonResponse(areas, safe=False)

def get_unity_check_list_type():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM unity_check_list_type")
        check_list_types = []
        for row in cursor.fetchall():
            check_list_type = {
                'id_ch_li_type': row[0],
                'name_ch_li_type': row[1]
            }
            check_list_types.append(check_list_type)
    return check_list_types

def logout_view(request):
    del request.session['username']
    del request.session['id_user_type']
    del request.session['department']
    return redirect('/login')

def checklist_form(request, id):
    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('checklist_item_sub')  # Get selected checkboxes
        remark = request.POST.get('remark', '')  # Get the value of "remark"

        if selected_checkboxes:
            with connection.cursor() as cursor:
                for value in selected_checkboxes:
                    # Combine the checkbox value and remark into one value before inserting into the database
                    if remark:
                        combined_value = f"{value}!{remark}"
                    else:
                        combined_value = value
                    cursor.execute("INSERT INTO unity_check_list_content (value) VALUES (%s)", [combined_value])
        return redirect('check_list_view')
    else:
        checklist_items = []
        with connection.cursor() as cursor:
            # Fetch the unity check list item based on the provided id
            cursor.execute("SELECT unity_check_list.id, department.department_name, area.area_name, unity_check_list.id_ch_list_type, unity_check_list_type.name_ch_type, date(unity_check_list.refdate) FROM unity_check_list LEFT OUTER JOIN department ON unity_check_list.id_department = department.id LEFT OUTER JOIN area ON unity_check_list.id_area = area.id LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id WHERE unity_check_list.id = %s", [id])
            unity_check = cursor.fetchone()

            # Fetch checklist items related to the unity check list item
            if unity_check[3] == 1:
                cursor.execute("""
                    SELECT 
                        CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER)
                            ELSE NULL 
                        END AS detail_check_list,
						unity_sub_item.id,
                        unity_item.unity_name, 
                        unity_check_list_type.name_ch_type, 
                        unity_item_detail.detail_name,
                        unity_sub_item.un_sub_num,
                        CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1') 
                    FROM unity_check_list_detail ucld 
                    LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                    LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                    LEFT OUTER JOIN unity_item_detail ON (
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) ~ '^\d+$' THEN unity_item_detail.id = CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER) 
                            ELSE FALSE 
                        END
                    ) 
                    LEFT OUTER JOIN unity_sub_item ON unity_item_detail.id = unity_sub_item.id_un_item_detail 
                    WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 1 AND id_un_ch_list = %s AND unity_item_detail.detail_name IS NOT NULL
                    Order by 
					header_check_list,detail_check_list,unity_sub_item.id 
                """, [id])
                checklist_items = cursor.fetchall()
            # Handle the second case for id_ch_list_type = 2
            elif unity_check[3] == 2:
                cursor.execute("""
                    SELECT 
                        CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN SPLIT_PART(ucld.check_list, '!', 3)
                            ELSE NULL 
                        END AS item_code,
                        unity_item.unity_name, 
                        unity_check_list_type.name_ch_type, 
                        unity_item_detail.detail_name,
						CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',unity_item_detail.id,'!','1') 
                    FROM unity_check_list_detail ucld 
                    LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                    LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                    LEFT OUTER JOIN unity_item_detail ON unity_item.id = unity_item_detail.id_unity_item 
                    WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 2 AND id_un_ch_list = %s
                """, [id])
                checklist_items = cursor.fetchall()
                # print(checklist_items)
            elif unity_check[3] == 3:
                cursor.execute("""
                               SELECT
                                CAST(SPLIT_PART(unity_check_list.itemcode, '!', 1) AS VARCHAR),
       							CAST(SPLIT_PART(unity_check_list.itemcode, '!', 2) AS VARCHAR),
       							CAST(SPLIT_PART(unity_check_list.itemcode, '!', 3) AS VARCHAR),
                                CONCAT (unity_check_list.id,'!',unity_check_list.id_ch_list_type,'!',EXTRACT(MONTH FROM CURRENT_DATE),'!','1','!',CURRENT_DATE),
                                CONCAT (unity_check_list.id,'!',unity_check_list.id_ch_list_type,'!',EXTRACT(MONTH FROM CURRENT_DATE),'!','2','!',CURRENT_DATE)
                                FROM unity_check_list
                                where unity_check_list.id = %s
                            """, [id])
                checklist_items = cursor.fetchall()
            elif unity_check[3] == 4:
                cursor.execute("""
                                SELECT 
                                    CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                    CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                                    unity_item.unity_name, 
                                    unity_check_list_type.name_ch_type, 
                                    unity_item_detail.detail_name,
            						CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',unity_item_detail.id,'!','1') 
                                FROM unity_check_list_detail ucld 
                                LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                                LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                                LEFT OUTER JOIN unity_item_detail ON unity_item.id = unity_item_detail.id_unity_item 
                                WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 4 AND id_un_ch_list = %s
                            """, [id])
                checklist_items = cursor.fetchall()

    return render(request, 'checklist.html', {'unity_check': unity_check, 'checklist_items': checklist_items})

def check_list_view(request):
    # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูล
    with connection.cursor() as cursor:
        cursor.execute("select unity_check_list.id,department.department_name,area.area_name,unity_check_list_type.name_ch_type,date(unity_check_list.refdate)  from unity_check_list left outer join department on unity_check_list.id_department = department.id left outer join area on unity_check_list.id_area = area.id left outer join  unity_check_list_type on unity_check_list.id_ch_list_type = unity_check_list_type.id ")
        check_list_data = cursor.fetchall()
        # print(check_list_data)
    return render(request, 'listchecklist.html', {'listchecklists': check_list_data})

def checklist_report(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT unity_check_list.id, department.department_name, area.area_name, unity_check_list.id_ch_list_type, unity_check_list_type.name_ch_type, date(unity_check_list.refdate),CAST(SPLIT_PART(unity_check_list.itemcode, '!', 4) AS VARCHAR) FROM unity_check_list LEFT OUTER JOIN department ON unity_check_list.id_department = department.id LEFT OUTER JOIN area ON unity_check_list.id_area = area.id LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id WHERE unity_check_list.id = %s",
            [id])
        unity_check = cursor.fetchone()
        report_data_ch = []
        if unity_check[3] == 1:
            cursor.execute("""
                            SELECT 
            						ucld.check_list,
            						uclc.value,
                                    CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                    CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                                    CASE 
                                        WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER)
                                        ELSE NULL 
                                    END AS detail_check_list,
            						unity_sub_item.id,
                                    unity_item.unity_name, 
                                    unity_item_detail.detail_name,
                                    unity_sub_item.un_sub_num,
                                    CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1'),
            						CAST(SPLIT_PART(uclc.value, '!', 3) AS INTEGER) AS Head,
            						CAST(SPLIT_PART(uclc.value, '!', 4) AS INTEGER) AS Subhead,
            						CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) AS LineDetail,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 1 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck1,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 2 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck2,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 3 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck3,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 4 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck4,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 5 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck5,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 6 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck6,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 7 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck7,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 8 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck8,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 9 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck9,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 10 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck10,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 11 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck11,
            						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 12 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck12

            					 FROM unity_check_list ucl
                            	LEFT OUTER JOIN unity_check_list_detail ucld ON ucl.id = ucld.id_un_ch_list
                                LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                                LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                                LEFT OUTER JOIN unity_item_detail ON (
                                    CASE 
                                        WHEN SPLIT_PART(ucld.check_list, '!', 3) ~ '^\d+$' THEN unity_item_detail.id = CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER) 
                                        ELSE FALSE 
                                    END
                                ) 
                                LEFT OUTER JOIN unity_sub_item ON unity_item_detail.id = unity_sub_item.id_un_item_detail 
                                LEFT OUTER JOIN unity_check_list_content  uclc ON CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' || split_part(uclc.value, '!', 4) || '!' || split_part(uclc.value, '!', 5) || '!' || split_part(uclc.value, '!', 6)
            					WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 1 AND id_un_ch_list = %s AND unity_item_detail.detail_name IS NOT NULL
                                GROUP BY ucld.check_list,
            						uclc.value,unity_item.id, ucld.id,uclc.value,ucld.check_list, Head, Subhead, LineDetail,detail_check_list,ucld.check_list,unity_sub_item.id,unity_item_detail.detail_name
            					Order by 
            					header_check_list,detail_check_list,unity_sub_item.id 
                            """, [id])

            rows = cursor.fetchall()

            # Process the rows and format the data as needed
            report_data = []

            for row in rows:
                    report_data.append({
                    'id': row[0],
                    'value': row[1],
                    'Head': row[6],
                    'subhead': row[7],
                    'LineDetail': row[8],
                    'valuecheck1': row[13],
                    'valuecheck2': row[14],
                    'valuecheck3': row[15],
                    'valuecheck4': row[16],
                    'valuecheck5': row[17],
                    'valuecheck6': row[18],
                    'valuecheck7': row[19],
                    'valuecheck8': row[20],
                    'valuecheck9': row[21],
                    'valuecheck10': row[22],
                    'valuecheck11': row[23],
                    'valuecheck12': row[24],
                })
        elif unity_check[3] == 2:
            cursor.execute("""
                            select 
                                ucld.id_un_ch_list,
        						ui.unity_name,
        						uid.detail_name,
        						CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                                CASE 
                                    WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS VARCHAR)
                                    ELSE NULL 
                                END AS detail_check_list,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 1 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck1,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 2 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck2,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 3 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck3,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 4 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck4,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 5 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck5,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 6 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck6,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 7 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck7,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 8 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck8,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 9 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck9,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 10 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck10,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 11 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck11,
        						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 12 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck12 
                            from unity_item ui
                            left outer join unity_item_detail uid on ui.id = uid.id_unity_item
                            left outer join unity_check_list_detail ucld on ui.id =  CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) and ucld.id_un_ch_list = %s
                            LEFT OUTER JOIN unity_check_list_content  uclc ON  CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',uid.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' || split_part(uclc.value, '!', 4) || '!' || split_part(uclc.value, '!', 5) || '!' || split_part(uclc.value, '!', 6)

                            where 
                                ui.unity_item_type = 2 
                            GROUP BY 
                                ui.unity_name,
                                uid.detail_name,
                                ucld.check_list,
                                uclc.value,
                                ui.id,
                                ucld.id,
                                uclc.value,
                                ucld.check_list,
                                header_check_list,
                                detail_check_list,
                                ucld.check_list,
                                uid.id
                            order by
                                uid.id_unity_item,detail_check_list,uid.id
                                        """, [id])

            rows = cursor.fetchall()

            # Process the rows and format the data as needed
            report_data = []

            for row in rows:
                report_data.append({
                    'id': row[0],
                    'value': row[1],
                    'Head': row[1],
                    'subhead': row[2],
                    'LineDetail': row[5],
                    'valuecheck1': row[6],
                    'valuecheck2': row[7],
                    'valuecheck3': row[8],
                    'valuecheck4': row[9],
                    'valuecheck5': row[10],
                    'valuecheck6': row[11],
                    'valuecheck7': row[12],
                    'valuecheck8': row[13],
                    'valuecheck9': row[14],
                    'valuecheck10': row[15],
                    'valuecheck11': row[16],
                    'valuecheck12': row[17],
                })
        elif unity_check[3] == 4:
            cursor.execute("""select 
                                    ucld.id_un_ch_list,
                                    ui.unity_name,
                                    uid.detail_name,
            						CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                    CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '1' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck1,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '2' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck2,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '3' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck3,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '4' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck4,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '5' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck5,
                					MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '1' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck1,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '2' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck2,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '3' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck3,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '4' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck4,
                                    MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '5' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck5

                                    from unity_item ui
                                    left outer join unity_item_detail uid on ui.id = uid.id_unity_item
                                    left outer join unity_check_list_detail ucld on ui.id =  CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) and ucld.id_un_ch_list = %s
                                    LEFT OUTER JOIN unity_check_list_content  uclc ON  CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',uid.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' ||split_part(uclc.value, '!', 4) || '!' ||split_part(uclc.value, '!', 5)  and DATE_PART('month', uclc.ref_date) = DATE_PART('month', current_date)

                                    where 
                                            ui.unity_item_type = 4 
                                    GROUP BY 
                                            ui.unity_name,
                                            uid.detail_name,
                                            ucld.check_list,
                                            uclc.value,
                                            ui.id,
                                            ucld.id,
                                            uclc.value,
                                            ucld.check_list,
                                            header_check_list,
                                            ucld.check_list,
                                            uid.id
                                            order by
                                            uid.id_unity_item
                            				""", [id])

            rows = cursor.fetchall()

            report_data = []

            for row in rows:
                    report_data.append({
                        'id': row[0],
                        'Head': row[1],
                        'subhead': row[2],
                        'valuecheck1': row[5],
                        'valuecheck2': row[6],
                        'valuecheck3': row[7],
                        'valuecheck4': row[8],
                        'valuecheck5': row[9],
                        'user_check1': row[10],
                        'user_check2': row[11],
                        'user_check3': row[12],
                        'user_check4': row[13],
                        'user_check5': row[14],
                    })
        elif unity_check[3] == 3:
            cursor.execute("""
                            SELECT 
                            unity_check_list.id, 
                            department.department_name, 
                            area.area_name, 
                            unity_check_list.id_ch_list_type, 
                            unity_check_list_type.name_ch_type, 
                            date(unity_check_list.refdate),
                            CAST(SPLIT_PART(unity_check_list.itemcode, '!', 1) AS VARCHAR),
       						CAST(SPLIT_PART(unity_check_list.itemcode, '!', 2) AS VARCHAR),
       						CAST(SPLIT_PART(unity_check_list.itemcode, '!', 3) AS VARCHAR)
                            FROM unity_check_list 
                            LEFT OUTER JOIN department ON unity_check_list.id_department = department.id 
                            LEFT OUTER JOIN area ON unity_check_list.id_area = area.id 
                            LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id 
                            WHERE unity_check_list.id = %s and unity_check_list.id_ch_list_type = 3 """, [id])

            # Process the rows and format the data as needed
            report_data = cursor.fetchone()
            cursor.execute("""
                            select 
                                        
                                    CAST(SPLIT_PART(uclc .value, '!', 1) AS INTEGER) AS id_check_list,
                                    CAST(SPLIT_PART(uclc .value, '!', 2) AS INTEGER) AS type_ch,
                                    CAST(SPLIT_PART(uclc .value, '!', 3) AS INTEGER) AS month_ch,
                                    CAST(SPLIT_PART(uclc .value, '!', 4) AS INTEGER) AS condition_ch,
                                    CAST(SPLIT_PART(uclc .value, '!', 5) AS date) AS date_ch,
                                    CAST(SPLIT_PART(uclc .value, '!', 6) AS varchar) AS remark
                
                                    from  unity_check_list_content  uclc 
                                    where 
                                    CAST(SPLIT_PART(uclc .value, '!', 1) AS INTEGER) = %s """, [id])
            report_data_ch = cursor.fetchall()

        return render(request, 'checklistreport.html', {'report_data': report_data , 'unity_check':unity_check,'report_data_ch':report_data_ch})

def m_checklist_report(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT unity_check_list.id, department.department_name, area.area_name, unity_check_list.id_ch_list_type, unity_check_list_type.name_ch_type, date(unity_check_list.refdate),CAST(SPLIT_PART(unity_check_list.itemcode, '!', 4) AS VARCHAR) FROM unity_check_list LEFT OUTER JOIN department ON unity_check_list.id_department = department.id LEFT OUTER JOIN area ON unity_check_list.id_area = area.id LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id WHERE unity_check_list.id = %s",
            [id])
        unity_check = cursor.fetchone()
        report_data_ch = []
        if unity_check[3] == 1:
            cursor.execute("""
                SELECT 
						ucld.check_list,
						uclc.value,
                        CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER)
                            ELSE NULL 
                        END AS detail_check_list,
						unity_sub_item.id,
                        unity_item.unity_name, 
                        unity_item_detail.detail_name,
                        unity_sub_item.un_sub_num,
                        CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1'),
						CAST(SPLIT_PART(uclc.value, '!', 3) AS INTEGER) AS Head,
						CAST(SPLIT_PART(uclc.value, '!', 4) AS INTEGER) AS Subhead,
						CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) AS LineDetail,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 1 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck1,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 2 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck2,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 3 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck3,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 4 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck4,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 5 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck5,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 6 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck6,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 7 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck7,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 8 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck8,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 9 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck9,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 10 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck10,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 11 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck11,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 12 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck12

					 FROM unity_check_list ucl
                	LEFT OUTER JOIN unity_check_list_detail ucld ON ucl.id = ucld.id_un_ch_list
                    LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                    LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                    LEFT OUTER JOIN unity_item_detail ON (
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) ~ '^\d+$' THEN unity_item_detail.id = CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER) 
                            ELSE FALSE 
                        END
                    ) 
                    LEFT OUTER JOIN unity_sub_item ON unity_item_detail.id = unity_sub_item.id_un_item_detail 
                    LEFT OUTER JOIN unity_check_list_content  uclc ON CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' || split_part(uclc.value, '!', 4) || '!' || split_part(uclc.value, '!', 5) || '!' || split_part(uclc.value, '!', 6)
					WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 1 AND id_un_ch_list = %s AND unity_item_detail.detail_name IS NOT NULL
                    GROUP BY ucld.check_list,
						uclc.value,unity_item.id, ucld.id,uclc.value,ucld.check_list, Head, Subhead, LineDetail,detail_check_list,ucld.check_list,unity_sub_item.id,unity_item_detail.detail_name
					Order by 
					header_check_list,detail_check_list,unity_sub_item.id 
                """, [id])

            rows = cursor.fetchall()

            # Process the rows and format the data as needed
            report_data = []

            for row in rows:
                report_data.append({
                    'id': row[0],
                    'value': row[1],
                    'Head': row[6],
                    'subhead': row[7],
                    'LineDetail': row[8],
                    'valuecheck1': row[13],
                    'valuecheck2': row[14],
                    'valuecheck3': row[15],
                    'valuecheck4': row[16],
                    'valuecheck5': row[17],
                    'valuecheck6': row[18],
                    'valuecheck7': row[19],
                    'valuecheck8': row[20],
                    'valuecheck9': row[21],
                    'valuecheck10': row[22],
                    'valuecheck11': row[23],
                    'valuecheck12': row[24],
                })
        elif unity_check[3] == 2:
            cursor.execute("""
                    select 
                        ucld.id_un_ch_list,
						ui.unity_name,
						uid.detail_name,
						CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS VARCHAR)
                            ELSE NULL 
                        END AS detail_check_list,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 1 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck1,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 2 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck2,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 3 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck3,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 4 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck4,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 5 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck5,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 6 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck6,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 7 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck7,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 8 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck8,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 9 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck9,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 10 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck10,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 11 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck11,
						MAX(CASE WHEN DATE_PART('month', uclc.ref_date) = 12 THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS INTEGER) END) AS valuecheck12 
                    from unity_item ui
                    left outer join unity_item_detail uid on ui.id = uid.id_unity_item
                    left outer join unity_check_list_detail ucld on ui.id =  CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) and ucld.id_un_ch_list = %s
                    LEFT OUTER JOIN unity_check_list_content  uclc ON  CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',uid.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' || split_part(uclc.value, '!', 4) || '!' || split_part(uclc.value, '!', 5) || '!' || split_part(uclc.value, '!', 6)

                    where 
                        ui.unity_item_type = 2 
                    GROUP BY 
                        ui.unity_name,
                        uid.detail_name,
                        ucld.check_list,
                        uclc.value,
                        ui.id,
                        ucld.id,
                        uclc.value,
                        ucld.check_list,
                        header_check_list,
                        detail_check_list,
                        ucld.check_list,
                        uid.id
                    order by
                        uid.id_unity_item,detail_check_list,uid.id
                                """, [id])

            rows = cursor.fetchall()

            # Process the rows and format the data as needed
            report_data = []

            for row in rows:
                report_data.append({
                    'id': row[0],
                    'value': row[1],
                    'Head': row[1],
                    'subhead': row[2],
                    'LineDetail': row[5],
                    'valuecheck1': row[6],
                    'valuecheck2': row[7],
                    'valuecheck3': row[8],
                    'valuecheck4': row[9],
                    'valuecheck5': row[10],
                    'valuecheck6': row[11],
                    'valuecheck7': row[12],
                    'valuecheck8': row[13],
                    'valuecheck9': row[14],
                    'valuecheck10': row[15],
                    'valuecheck11': row[16],
                    'valuecheck12': row[17],
                })
        elif unity_check[3] == 4:
            cursor.execute("""select 
                                            ucld.id_un_ch_list,
                    						ui.unity_name,
                    						uid.detail_name,
                    						CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                            CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '1' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck1,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '2' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck2,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '3' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck3,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '4' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck4,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '5' THEN CAST(SPLIT_PART(uclc.value, '!', 5) AS INTEGER) END) AS valuecheck5,
											MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '1' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck1,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '2' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck2,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '3' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck3,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '4' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck4,
                    						MAX(CASE WHEN to_char(uclc.ref_date, 'W') = '5' THEN CAST(SPLIT_PART(uclc.value, '!', 6) AS varchar) END) AS usercheck5
                                        
                                        from unity_item ui
                                        left outer join unity_item_detail uid on ui.id = uid.id_unity_item
                                        left outer join unity_check_list_detail ucld on ui.id =  CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) and ucld.id_un_ch_list = %s
                                        LEFT OUTER JOIN unity_check_list_content  uclc ON  CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',uid.id,'!','1') = split_part(uclc.value, '!', 1) || '!' || split_part(uclc.value, '!', 2) || '!' || split_part(uclc.value, '!', 3) || '!' ||split_part(uclc.value, '!', 4) || '!' ||split_part(uclc.value, '!', 5)  and DATE_PART('month', uclc.ref_date) = DATE_PART('month', current_date)

                                        where 
                                            ui.unity_item_type = 4 
                                        GROUP BY 
                                            ui.unity_name,
                                            uid.detail_name,
                                            ucld.check_list,
                                            uclc.value,
                                            ui.id,
                                            ucld.id,
                                            uclc.value,
                                            ucld.check_list,
                                            header_check_list,
                                            ucld.check_list,
                                            uid.id
                                        order by
                                            uid.id_unity_item


            							""", [id])

            rows = cursor.fetchall()

            report_data = []

            for row in rows:
                    report_data.append({
                        'id': row[0],
                        'Head': row[1],
                        'subhead': row[2],
                        'valuecheck1': row[5],
                        'valuecheck2': row[6],
                        'valuecheck3': row[7],
                        'valuecheck4': row[8],
                        'valuecheck5': row[9],
                        'user_check1': row[10],
                        'user_check2': row[11],
                        'user_check3': row[12],
                        'user_check4': row[13],
                        'user_check5': row[14],
                    })
        elif unity_check[3] == 3:
            cursor.execute("""
                                   SELECT 
                                   unity_check_list.id, 
                                   department.department_name, 
                                   area.area_name, 
                                   unity_check_list.id_ch_list_type, 
                                   unity_check_list_type.name_ch_type, 
                                   date(unity_check_list.refdate),
                                   CAST(SPLIT_PART(unity_check_list.itemcode, '!', 1) AS VARCHAR),
       							   CAST(SPLIT_PART(unity_check_list.itemcode, '!', 2) AS VARCHAR),
       							   CAST(SPLIT_PART(unity_check_list.itemcode, '!', 3) AS VARCHAR)
                                   FROM unity_check_list 
                                   LEFT OUTER JOIN department ON unity_check_list.id_department = department.id 
                                   LEFT OUTER JOIN area ON unity_check_list.id_area = area.id 
                                   LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id 
                                   WHERE unity_check_list.id = %s and unity_check_list.id_ch_list_type = 3 """, [id])

            # Process the rows and format the data as needed
            report_data = cursor.fetchone()
            cursor.execute("""
                                   select 

                                           CAST(SPLIT_PART(uclc .value, '!', 1) AS INTEGER) AS id_check_list,
                                           CAST(SPLIT_PART(uclc .value, '!', 2) AS INTEGER) AS type_ch,
                                           CAST(SPLIT_PART(uclc .value, '!', 3) AS INTEGER) AS month_ch,
                                           CAST(SPLIT_PART(uclc .value, '!', 4) AS INTEGER) AS condition_ch,
                                           CAST(SPLIT_PART(uclc .value, '!', 5) AS date) AS date_ch,
                                           CAST(SPLIT_PART(uclc .value, '!', 6) AS varchar) AS remark,
										   CAST(SPLIT_PART(uclc .value, '!', 7) AS varchar) AS name_ch

                                           from  unity_check_list_content  uclc 
                                           where 
                                           CAST(SPLIT_PART(uclc .value, '!', 1) AS INTEGER) = %s """, [id])
            report_data_ch = cursor.fetchall()


        return render(request, 'M_checklistreport.html',{'report_data': report_data, 'unity_check': unity_check, 'report_data_ch': report_data_ch})

def M_checklist_form(request, id):
    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('checklist_item_sub')  # Get selected checkboxes
        remark = request.POST.get('remark', '')  # Get the value of "remark"
        user_id = request.session.get('M_username')
        if selected_checkboxes:
            with connection.cursor() as cursor:
                for value in selected_checkboxes:
                    # Combine the checkbox value and remark into one value before inserting into the database
                    if remark:
                        combined_value = f"{value}!{user_id}!{remark}"
                    else:
                        combined_value = f"{value}!{user_id}"
                    cursor.execute("INSERT INTO unity_check_list_content (value) VALUES (%s)", [combined_value])
        return redirect('M_checklist_report', id=id)
    else:
        checklist_items = []
        with connection.cursor() as cursor:
            # Fetch the unity check list item based on the provided id
            cursor.execute("SELECT unity_check_list.id, department.department_name, area.area_name, unity_check_list.id_ch_list_type, unity_check_list_type.name_ch_type, date(unity_check_list.refdate) FROM unity_check_list LEFT OUTER JOIN department ON unity_check_list.id_department = department.id LEFT OUTER JOIN area ON unity_check_list.id_area = area.id LEFT OUTER JOIN unity_check_list_type ON unity_check_list.id_ch_list_type = unity_check_list_type.id WHERE unity_check_list.id = %s", [id])
            unity_check = cursor.fetchone()

            # Fetch checklist items related to the unity check list item
            if unity_check[3] == 1:
                cursor.execute("""
                    SELECT 
                        CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER)
                            ELSE NULL 
                        END AS detail_check_list,
						unity_sub_item.id,
                        unity_item.unity_name, 
                        unity_check_list_type.name_ch_type, 
                        unity_item_detail.detail_name,
                        unity_sub_item.un_sub_num,
                        CONCAT (id_un_ch_list,'!',ucld.check_list,'!',unity_sub_item.id,'!','1') 
                    FROM unity_check_list_detail ucld 
                    LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                    LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                    LEFT OUTER JOIN unity_item_detail ON (
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) ~ '^\d+$' THEN unity_item_detail.id = CAST(SPLIT_PART(ucld.check_list, '!', 3) AS INTEGER) 
                            ELSE FALSE 
                        END
                    ) 
                    LEFT OUTER JOIN unity_sub_item ON unity_item_detail.id = unity_sub_item.id_un_item_detail 
                    WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 1 AND id_un_ch_list = %s AND unity_item_detail.detail_name IS NOT NULL
                    Order by 
					header_check_list,detail_check_list,unity_sub_item.id 
                """, [id])
                checklist_items = cursor.fetchall()

            # Handle the second case for id_ch_list_type = 2
            elif unity_check[3] == 2:
                cursor.execute("""
                    SELECT 
                        CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                        CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                        CASE 
                            WHEN SPLIT_PART(ucld.check_list, '!', 3) <> '' THEN SPLIT_PART(ucld.check_list, '!', 3)
                            ELSE NULL 
                        END AS item_code,
                        unity_item.unity_name, 
                        unity_check_list_type.name_ch_type, 
                        unity_item_detail.detail_name,
						CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',unity_item_detail.id,'!','1') 
                    FROM unity_check_list_detail ucld 
                    LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                    LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                    LEFT OUTER JOIN unity_item_detail ON unity_item.id = unity_item_detail.id_unity_item 
                    WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 2 AND id_un_ch_list = %s
                """, [id])
                checklist_items = cursor.fetchall()
            elif unity_check[3] == 3:
                cursor.execute("""
                                           SELECT
                                            CAST(SPLIT_PART(unity_check_list.itemcode, '!', 1) AS VARCHAR),
                                            CAST(SPLIT_PART(unity_check_list.itemcode, '!', 2) AS VARCHAR),
                                            CAST(SPLIT_PART(unity_check_list.itemcode, '!', 3) AS VARCHAR),
                                            CONCAT (unity_check_list.id,'!',unity_check_list.id_ch_list_type,'!',EXTRACT(MONTH FROM CURRENT_DATE),'!','1','!',CURRENT_DATE),
                                            CONCAT (unity_check_list.id,'!',unity_check_list.id_ch_list_type,'!',EXTRACT(MONTH FROM CURRENT_DATE),'!','2','!',CURRENT_DATE)
                                            FROM unity_check_list
                                            where unity_check_list.id = %s
                                        """, [id])
                checklist_items = cursor.fetchall()
            elif unity_check[3] == 4:
                cursor.execute("""
                                SELECT 
                                    CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) AS type_check_list,
                                    CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) AS header_check_list,
                                    unity_item.unity_name, 
                                    unity_check_list_type.name_ch_type, 
                                    unity_item_detail.detail_name,
            						CONCAT (ucld.id_un_ch_list,'!',ucld.check_list,'!',unity_item_detail.id,'!','1') 
                                FROM unity_check_list_detail ucld 
                                LEFT OUTER JOIN unity_item ON unity_item.id = CAST(SPLIT_PART(ucld.check_list, '!', 2) AS INTEGER) 
                                LEFT OUTER JOIN unity_check_list_type ON unity_check_list_type.id = CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) 
                                LEFT OUTER JOIN unity_item_detail ON unity_item.id = unity_item_detail.id_unity_item 
                                WHERE CAST(SPLIT_PART(ucld.check_list, '!', 1) AS INTEGER) = 4 AND id_un_ch_list = %s
                            """, [id])
                checklist_items = cursor.fetchall()
        return render(request, 'M_checklist.html', {'unity_check': unity_check, 'checklist_items': checklist_items})

# def M_login_view(request):
#     if request.method == 'POST':
#         M_username = request.POST['username']
#         M_password = request.POST['password']
#         # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM user_login WHERE username = %s AND password = %s", [M_username, M_password])
#             M_user_data = cursor.fetchone()
#         if M_user_data is not None:
#             # การยืนยันสำเร็จ ดำเนินการตามที่ต้องการ เช่น เก็บข้อมูลผู้ใช้งานใน session และเปลี่ยนเส้นทางไปยังหน้าหลังเข้าสู่ระบบ
#             request.session['M_id_user_type'] = M_user_data[3]
#             request.session['M_username'] = M_user_data[1]# เก็บค่า id_user_type ใน session
#             if 'next' in request.GET:
#                 next_url = request.GET['next']
#                 return redirect(next_url)
#             else:
#                 return redirect('M_checklist_report')
#         else:
#             error_message = 'กรุณาตรวจสอบ Username เเละ Password ให้ถูกต้อง'
#             return render(request, 'M_login.html', {'error_message': error_message})
#     return render(request, 'M_login.html')

def M_login_view(request):
    if request.method == 'POST':
        M_username = request.POST['username']
        M_password = request.POST['password']
        md5_password = hashlib.md5(M_password.encode()).hexdigest().upper()

        # ดำเนินการที่จำเป็นสำหรับการเชื่อมต่อกับฐานข้อมูลและดึงข้อมูลผู้ใช้งาน
        with connections['default'].cursor() as cursor:
            # ดึงข้อมูลผู้ใช้จากตาราง user_login
            cursor.execute("SELECT * FROM user_login WHERE username = %s", [M_username])
            M_user_login_data = cursor.fetchone()

            if M_user_login_data is not None:
                # หากมีผู้ใช้งานในตาราง user_login
                # เช็ครหัสผ่านจากตาราง user_list
                with connections['user_list'].cursor() as cursor_user_list:
                    cursor_user_list.execute("SELECT * FROM user_list ul WHERE ul.id = %s AND ul.password = %s",
                                             [M_username, md5_password])
                    M_user_data = cursor_user_list.fetchone()

                    if M_user_data is not None:
                        # การยืนยันสำเร็จ ดำเนินการตามที่ต้องการ เช่น เก็บข้อมูลผู้ใช้งานใน session และเปลี่ยนเส้นทางไปยังหน้าหลังเข้าสู่ระบบ
                        request.session['M_id_user_type'] = M_user_login_data[3]
                        request.session['M_username'] = M_user_data[0]
                        if 'next' in request.GET:
                            next_url = request.GET['next']
                            return redirect(next_url)
                        else:
                            return redirect('M_checklist_report')
                    else:
                        error_message = 'รหัสผ่านไม่ถูกต้อง'
            else:
                error_message = 'Username ไม่ถูกต้อง'

            return render(request, 'M_login.html', {'error_message': error_message})

    return render(request, 'M_login.html')

def M_logout_view(request):
    del request.session['M_id_user_type']
    del request.session['M_department']
    del request.session['M_username']
    id = request.GET.get('id')  # รับ ID จากพารามิเตอร์
    return redirect(f'/M_checklist_report/{id}/')

